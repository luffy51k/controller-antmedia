from celery import Celery


def make_celery(app=None):
    """
    Make Celery App
    :param app: flask app instance
    :return: celery
    """

    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        timezone="Asia/Ho_Chi_Minh",
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        include=["apps.worker.tasks"],
    )

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
