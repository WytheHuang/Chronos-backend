from config.celery import app


@app.task
def hello_world():
    """Just a simple example."""
    print("Hello World!")  # noqa: T201
    return "Hello World!"
