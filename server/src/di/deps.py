import logging

from src.db import Database
from src.svc import Detector, QueryBuilder, SupabaseClient

class Dependencies:
    def __init__(
        self,
        detector: Detector = None,
        db: Database = None,
        qb: QueryBuilder = None,
        sbc: SupabaseClient = None
    ):
        self._detector = detector
        self._db = db
        self._qb = qb
        self._sbc = sbc
        
        logging.info("Dependencies initialized")
    
    def get_detector(self) -> Detector:
        return self._detector
    
    def get_db(self) -> Database:
        return self._db
    
    def get_qb(self) -> QueryBuilder:
        return self._qb
    
    def get_sbc(self) -> SupabaseClient:
        return self._sbc