import logging
from src.svc.ner import Detector
from src.db.conn import Database

class Dependencies:
    def __init__(
        self,
        detector: Detector = None,
        db: Database = None,
    ):
        self.detector = detector
        self.db = db
        
        logging.info("Dependencies initialized")
    
    def get_detector(self) -> Detector:
        return self.detector