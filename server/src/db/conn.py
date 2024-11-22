import logging
from typing import List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection, Result
from sqlalchemy.exc import SQLAlchemyError

class Database:
    def __init__(self, uri: str) -> None:
        try:
            self.uri = uri
            self.engine: Engine = self._create_engine()
            logging.info("Database initialized")
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise
        

    def _create_engine(self) -> Engine:
        return create_engine(self.uri)

    def get_connection(self) -> Connection:
        conn = self.engine.connect()
        return conn

    def execute(self, sql: str, params: Optional[dict] = None, withTx: bool = False) -> Result:
        try:
            with self.get_connection() as conn:
                if withTx:
                    with conn.begin():
                        result = conn.execute(text(sql), params or {})
                else:
                    result = conn.execute(text(sql), params or {})
                    
                return result
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            raise

    def query(self, sql: str, params: Optional[dict] = None) -> List[dict]:
        try:
            result = self.execute(sql, params)
            return [dict(row) for row in result]
        except SQLAlchemyError as e:
            print(f"Query error: {e}")
            raise

    def close(self) -> None:
        self.engine.dispose()