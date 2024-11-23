from celery import Celery
import logging

class Enqueuer:
    def __init__(self, broker: str):
        self.celery = Celery('Task Enqueuer', broker=broker)
        logging.info("Celery Worker initialized")

    def enqueue_task(
        self,
        task_name: str,
        args: list = [],
        task_args: dict = {},
    ):
        self.celery.send_task(
            task_name,
            args=args,
            kwargs=task_args,
        )