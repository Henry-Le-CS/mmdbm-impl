import os
import logging
from dotenv import load_dotenv

from src.svc.worker.task_registry import TaskRegistry
from src.svc.worker.tasks import register_tasks

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = register_tasks(TaskRegistry(broker=os.getenv("CELERY_BROKER"))).get_app()
    
if __name__ == "__main__":
    logging.info("Worker starting...")    
    app.start()