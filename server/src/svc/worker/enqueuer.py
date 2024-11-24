import uuid
import logging
from celery import Celery

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
        job_id = uuid.uuid4()
        # The first argument of the task is the job_id
        args = [job_id] + args
        self.celery.send_task(
            task_name,
            args=args,
            kwargs=task_args,
        )
                
        return job_id