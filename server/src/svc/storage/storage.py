import os
import logging

class StorageService:
    def __init__(self, folder: str = "storage") -> None:
        self.storage_path = os.getcwd() + "/" + folder
        self._init_folder()
        logging.info("StorageService initialized")
        
    def _init_folder(self):
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            logging.info(f"Folder {self.storage_path} created")
        