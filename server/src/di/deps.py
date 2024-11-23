import logging


class Dependencies:
    def __init__(
        self,
        detector = None,
        db= None,
        qb = None,
        sbc = None,
        storage_svc = None,
        task_enqueuer = None
    ):
        self._detector = detector
        self._db = db
        self._qb = qb
        self._sbc = sbc
        self._storage_svc = storage_svc
        self._task_enqueuer = task_enqueuer
          
        logging.info("Dependencies initialized")
    
    def get_detector(self):
        return self._detector
    
    def get_db(self):
        return self._db
    
    def get_qb(self):
        return self._qb
    
    def get_sbc(self):
        return self._sbc
    
    def get_storage_svc(self):
        return self._storage_svc
    
    def get_task_enqueuer(self):
        return self._task_enqueuer
        