from . import celery


@celery.task
def test():
    return "Done"
