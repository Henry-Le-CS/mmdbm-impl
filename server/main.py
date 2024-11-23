import os
import logging
from dotenv import load_dotenv

from src.di.deps import Dependencies
from src.db import Database
from src.svc.ner import Detector
from src.svc.qb import QueryBuilder

from src.http import Server
from src.api import new_api_registry

load_dotenv()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    server = new_api_registry(Server(
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=os.getenv("SERVER_PORT", 5001),
        debug=os.getenv("SERVER_DEBUG_MODE", False),
        deps=Dependencies(
            detector=Detector(),
            db=Database(os.getenv("DATABASE_URI")),
            qb=QueryBuilder()
        )
    ))

    server.run()
