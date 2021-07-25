from orginizer1_5.celery import app


@app.task
def add(x, y):
    return (x + y)