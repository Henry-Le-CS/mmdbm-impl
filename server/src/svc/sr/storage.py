import os
import logging
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import InternalServerError

from datetime import datetime

class StorageService:
    def __init__(self, folder: str = "storage") -> None:
        self.storage_path = os.path.join(os.getcwd(), folder)
        self._init_folder()
        logging.info("StorageService initialized")

    def _init_folder(self):
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            logging.info(f"Folder {self.storage_path} created")
    
    def _generate_file_metadata(self, file_name: str, file_size: int) -> dict:        
        return {
            "file_name": file_name,
            "file_size": file_size,
            "upload_time": datetime.utcnow().isoformat(),
            "storage_path": os.path.join(self.storage_path, file_name)
        }

    def save_file(self, file: FileStorage, metadata: dict = None) -> dict:
        try:
            filename = str(uuid.uuid4()) + "_" + file.filename
            file_path = os.path.join(self.storage_path, filename)
            file.save(file_path)
            
            return self._generate_file_metadata(filename, os.path.getsize(file_path))
        except Exception as e:
            raise e

    def remove_file(self, file_path: str):
        retries = 3
        while retries > 0:
            try:
                os.remove(file_path)
                break
            except Exception as e:
                logging.warning(f"Error removing file: {e}")
                retries -= 1
                if retries == 0:
                    raise e