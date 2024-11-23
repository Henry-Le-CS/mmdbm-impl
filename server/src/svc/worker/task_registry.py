from celery import Celery

class TaskRegistry:
    def __init__(self, broker: str):
        self.celery = Celery('Task Handler', broker=broker)
        pass
    
    def register(self, task_name: str, handler) -> "TaskRegistry":
        self.celery.task(name=task_name)(handler)
        return self
    
    def get_app(self):
        return self.celery