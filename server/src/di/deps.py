import logging

from src.db import Database
from src.svc import Detector, QueryBuilder, SupabaseClient, StorageService
class Dependencies:
    def __init__(
        self,
        detector: Detector = None,
        db: Database = None,
        qb: QueryBuilder = None,
        sbc: SupabaseClient = None,
        storage_svc: StorageService = None
    ):
        self._detector = detector
        self._db = db
        self._qb = qb
        self._sbc = sbc
        self._storage_svc = storage_svc
          
        logging.info("Dependencies initialized")
    
    def get_detector(self) -> Detector:
        return self._detector
    
    def get_db(self) -> Database:
        return self._db
    
    def get_qb(self) -> QueryBuilder:
        return self._qb
    
    def get_sbc(self) -> SupabaseClient:
        return self._sbc
    
    def get_storage_svc(self) -> StorageService:
        return self._storage_svc