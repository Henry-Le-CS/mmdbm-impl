import logging
from src.svc.ner import Detector
from src.db.conn import Database
from src.svc.qb import QueryBuilder

class Dependencies:
    def __init__(
        self,
        detector: Detector = None,
        db: Database = None,
        qb: QueryBuilder = None
    ):
        self._detector = detector
        self._db = db
        self._qb = qb
        
        logging.info("Dependencies initialized")
    
    def get_detector(self) -> Detector:
        return self._detector
    
    def get_db(self) -> Database:
        return self._db
    
    def get_qb(self) -> QueryBuilder:
        return self._qb