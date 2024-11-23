from flask import Flask
from typing import List

from src.http.chain import Chain
from src.http.middleware import Middleware
from src.di.deps import Dependencies


class Server:
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 5001,
        deps: Dependencies = None,
        debug: bool = False,
    ) -> None:
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.deps = deps
        self.debug = debug

    def register_route(
        self, 
        route: str, 
        handler: callable,
        endpoint: str,
        middlewares: List[Middleware] = [], 
        methods: List[str] = ["GET"],
    ):        
        self.app.route(
                route, 
                methods=methods,
                endpoint=endpoint
        )(Chain(
            self.deps,            
            middlewares, 
            handler
        ))
        
        return self

    def run(self) -> None:
        print(f"Starting server at {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=self.debug)
