from uuid import UUID
from django import core

from ninja import Schema
from ninja import ModelSchema

from core import utils as core_utils

from . import models


class CategoryModelSchema(ModelSchema):
    """Schema class for categories."""

    class Config:
        model = models.CategoryModel
        model_exclude = core_utils.BASE_EXCLUDE_FIELD


class CreateCategoryRequestSchema(Schema):
    name: str


class FileUploadLogModelSchema(Schema):
    """Schema class for file upload logs.

    This class defines the data structure for logs created during file uploads,
    including details like file identifier, storage key, creation time, processing status,
    file name, and uploader information.

    Args:
        id (UUID): Unique identifier for the file upload.
        s3_key (str): S3 storage key for the file.
        created_at (str): Timestamp of file upload.
        embeddings_status (str): Status of file processing.
        file_name (str): Name of the uploaded file.
        upload_by (str): User who uploaded the file.
    """

    id: UUID
    s3_key: str
    created_at: str
    embeddings_status: str
    category: str
    file_name: str
    upload_by: str


class FileUploadResponseSchema(Schema):
    """Schema for the response of a file upload operation.

    This schema provides the details of the response after a file has been uploaded,
    primarily focusing on the embedding task initiated by the upload.

    Args:
        embedding_task_id (str): Identifier of the embedding task started post-upload.
    """

    embedding_task_id: str


class EmbeddingStatusResponseSchema(Schema):
    """Schema for the response of an embedding task status query.

    This schema is used to convey the current status of an embedding task.

    Args:
        status (str): The current status of the embedding task.
    """

    status: str


class GenerativeAIDocumentRequestSchema(Schema):
    """Schema for a request to generate a document using AI.

    This schema defines the structure of a request for document generation, including
    the question and any reference documents.

    Args:
        question (str): The question or prompt for document generation.
        documents (list[str]): A list of reference documents.
    """

    question: str
    documents: list[str]
    model: str = "gpt-3.5-16k-turbo"


class GenerativeAIDocumentResponseSchema(Schema):
    """Schema for the response to a generative AI document request.

    This schema details the structure of the response from a document generation request,
    including a message and the location of the generated document.

    Args:
        message (str): A message or description of the response.
        s3_key (str): The S3 key where the generated document is stored.
    """

    message: str
    s3_key: str


class AskDocumentRequestSchema(Schema):
    """Schema for a request to the 'Ask Document' service.

    Defines the structure for a query to ask questions with optional filter categories
    and documents.

    Args:
        question (str): The question to be asked.
        filter_categories (list[str]): Optional categories to filter the response.
        filter_docs (list[str]): Optional document identifiers to refine the search.
    """

    question: str
    filter_categories: list[str] = []
    filter_docs: list[str] = []


class AskDocumentResponseSchema(Schema):
    """Schema for the response from the 'Ask Document' service.

    Details the structure of the response to a query, including the question, answer,
    and reference information.

    Args:
        Question (str): The original question asked.
        Answer (str): The provided answer to the question.
        References (dict]): Related reference documents or information.
    """

    Question: str
    Answer: str
    References: dict = {}


class DownloadByStringRequestSchema(Schema):
    """Schema for a request to download content based on a string identifier.

    This schema defines the format for requests to download specific content, identified
    by a string.

    Args:
        string (str): The string identifier used to locate and download the content.
    """

    string: str
