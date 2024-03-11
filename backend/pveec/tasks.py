from typing import Any
from typing import Literal

import requests
from config.celery import app
from django.conf import settings
from langchain.docstore.document import Document as LangchainDocument
from langchain_community.vectorstores import Qdrant
from qdrant_client.http import models as rest

from . import utils


# TODO(Stephen/Jen): try to fix ruff: PLR0915, C901 error
@app.task(bind=True, name="pveec.tasks.embding_task")
def embding_task(  # noqa: C901, PLR0915
    self,  # noqa: ARG001, ANN001
    s3_key: str,
):
    """The task for embedding document.

    All steps:
    1. get document from S3
    2. extract text from document
    3. extract embeddings from text
    4. save embeddings to Qdrant
    """

    def _replace_special_characters(text: str) -> str:
        sequences_to_replace = ["", "\u3000", "\n", "\t"]
        for seq in sequences_to_replace:
            text = text.replace(seq, "")
        return text

    def _url_check(url: str) -> bool:
        try:
            response = requests.get(url)  # noqa: S113
            if response.status_code == 200:  # noqa: PLR2004
                # print(f"{url} is operating successfully.")
                return True
            else:  # noqa: RET505
                # print(f"{url}'s status code is: {response.status_code}")
                pass
        except requests.exceptions.RequestException:
            # print(f"{url} is error, please check again: {e}")
            pass

        return False

    def _list_collections(url: str) -> list[Any] | str:
        endpoint = f"{url}/collections"
        response = requests.get(endpoint)  # noqa: S113

        if response.status_code == 200:  # noqa: PLR2004
            collections = response.json().get("result", {}).get("collections", [])
            return [collection["name"] for collection in collections]
        else:  # noqa: RET505
            return f"Error: {response.status_code}"

    # TODO(Stephen/Jen): current_h4, current_h5 還可以做, and tty to fix ruff: PLR0912, C901 error
    def _classify_paragraphs_by_level(  # noqa: PLR0912, C901
        doc: Any,
    ) -> dict[str, dict[str, dict[str, dict[Any, Any]]]]:
        current_h1 = None
        current_h2 = None
        current_h3 = None
        paragraphs_by_level = {"None": {"None": {"None": {}}}}
        for paragraph in doc.paragraphs:
            # print(f"paragraph: {paragraph}")
            style_name = paragraph.style.name
            text = paragraph.text
            # print(f"paragraph text: {text}")
            if text.lower() in ["", "\u3000", "\n", "\t"]:
                continue

            if style_name.startswith("Heading 1"):
                current_h1 = text
                current_h2 = None
                current_h3 = None

                if current_h1 not in paragraphs_by_level:
                    paragraphs_by_level[current_h1] = {}
                    paragraphs_by_level[current_h1]["None"] = {}
                    paragraphs_by_level[current_h1]["None"]["None"] = {}

            elif style_name.startswith("Heading 2"):
                current_h2 = text
                current_h3 = None
                h1 = current_h1
                if current_h1 is None:
                    h1 = "None"
                if current_h2 not in paragraphs_by_level[h1]:  # type: ignore
                    paragraphs_by_level[h1][current_h2] = {}  # type: ignore
                    paragraphs_by_level[h1][current_h2]["None"] = {}  # type: ignore

            elif style_name.startswith("Heading 3"):
                current_h3 = text
                h1 = current_h1
                h2 = current_h2
                if current_h1 is None:
                    h1 = "None"
                if current_h2 is None:
                    h2 = "None"
                if current_h3 not in paragraphs_by_level[h1][h2]:  # type: ignore
                    paragraphs_by_level[h1][h2][current_h3] = {}  # type: ignore

            else:
                current_level = {}
                if not current_h1:
                    current_h1 = "None"
                if not current_h2:
                    current_h2 = "None"
                if not current_h3:
                    current_h3 = "None"

                current_level = paragraphs_by_level[current_h1][current_h2][current_h3]

                processed_text = _replace_special_characters(text)
                if style_name in current_level:
                    current_level[style_name].append(processed_text)
                else:
                    current_level[style_name] = [processed_text]

        return paragraphs_by_level

    def _document_recursive(
        documents_list: list[LangchainDocument],
        value_dict: dict,
        doc_metadata: dict,
        parent_keys_str: str,
        indent: str = "",
    ) -> list[LangchainDocument] | Any:
        for key, value in value_dict.items():
            current_keys_str = f"{parent_keys_str}/{key}"

            if (key is None) or (key == "None"):
                current_keys_str = parent_keys_str
                # print(f"key is {type(key)}, current_keys_str: {current_keys_str}")

            if isinstance(value, dict):
                documents_list = _document_recursive(
                    documents_list,
                    value,
                    doc_metadata,
                    current_keys_str,
                    indent + "  ",
                )

            else:
                # Save the doc list of paragraphs into documents_list of this document
                doc_metadata["段落"] = current_keys_str
                for paragraph in value:
                    new_doc = LangchainDocument(page_content=paragraph, metadata={"source": doc_metadata})
                    documents_list.append(new_doc)
                    # print(f"documents_list: {documents_list}")

        return documents_list

    # Call the EmbeddingProcessor class to do embedding
    def _recreate_embedding_and_save(
        documents_list: list[LangchainDocument],
        qdrant_url: str,
        collection_name: str,
        embeddings: Any,
    ) -> Any:
        return Qdrant.from_documents(
            documents_list,
            embeddings,
            url=qdrant_url,
            prefer_grpc=False,
            collection_name=collection_name,
            force_recreate=True,
        )

    def _add_exsisting_embedding_and_save(
        documents_list: list[LangchainDocument],
        qdrant_url: str,
        collection_name: str,
        embeddings: Any,
    ) -> Any:
        return Qdrant.from_documents(
            documents_list,
            embeddings,
            url=qdrant_url,
            prefer_grpc=False,
            collection_name=collection_name,
            force_recreate=False,
        )

    def _embedding_process(
        documents_list: list[LangchainDocument],
        qdrant_url: str,
        collection_name: str,
        embeddings: Any,
        save_type: str = "Existing",
    ) -> Any | Literal[False]:
        if _url_check(qdrant_url):
            existing_collections = _list_collections(qdrant_url)
            if (save_type == "Existing") and (collection_name in existing_collections):
                qdrant = _add_exsisting_embedding_and_save(
                    documents_list=documents_list,
                    qdrant_url=qdrant_url,
                    collection_name=collection_name,
                    embeddings=embeddings,
                )
            elif save_type == "Recreate":
                qdrant = _recreate_embedding_and_save(
                    documents_list=documents_list,
                    qdrant_url=qdrant_url,
                    collection_name=collection_name,
                    embeddings=embeddings,
                )
            else:
                qdrant = _add_exsisting_embedding_and_save(
                    documents_list=documents_list,
                    qdrant_url=qdrant_url,
                    collection_name=collection_name,
                    embeddings=embeddings,
                )
            # print("All docs are processed successfully!")
            return qdrant
        else:  # noqa: RET505
            # print("Embedding  unsuccessfully!")
            return False

    # The main function for embeddings
    def _main_embedding(  # noqa: PLR0913
        category_name: str,
        doc_name: str,
        doc_file: Any,
        save_type: str = "Exsisting",
        qdrant_url: str = settings.QDRANT_URL,
        collection_name: str = settings.QDRANT_COLLECTION,
        embeddings: Any = utils.OPENAI_EMBEDDING,
    ) -> Any | Literal[False]:
        # Preprocess the doc_file into docx format
        if ".pdf" in doc_name:
            # print(f"Receive the pdf files.")
            doc_file = utils.pdf_to_docx(doc_file)
        if isinstance(doc_file, bytes):
            doc_file = utils.bytes_to_docx(doc_file)

        # Start the classifying process
        paragraphs_by_level = _classify_paragraphs_by_level(doc_file)
        # print(f"paragraphs_by_level: {paragraphs_by_level}")

        # Pack it into Document type
        documents_list = _document_recursive(
            documents_list=[],
            parent_keys_str="",
            value_dict=paragraphs_by_level,
            doc_metadata={
                "分類名稱": category_name if category_name is not None else "其他",
                "文件名稱": doc_name,
            },
        )

        return _embedding_process(
            documents_list=documents_list,
            qdrant_url=qdrant_url,
            collection_name=collection_name,
            embeddings=embeddings,
            save_type=save_type,
        )

    # Impletion function
    file_info = utils.get_file_info(s3_key)
    doc_file = utils.s3.get_object(Bucket=settings.AWS_S3_BUCKET_NAME, Key=s3_key)

    _main_embedding(
        category_name=file_info["category"],
        doc_name=file_info["filename"],
        doc_file=doc_file["Body"].read(),
        save_type="Exsisting",
        qdrant_url=settings.QDRANT_URL,
        collection_name=settings.QDRANT_COLLECTION,
    )
