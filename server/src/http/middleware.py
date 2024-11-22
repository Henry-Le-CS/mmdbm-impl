from typing import Callable, Any
from src.di.deps import Dependencies

class Middleware:
    def __init__(self, handler: Callable[[Any, dict, Callable], Any]) -> None:
        self.handler = handler

    def Exec(self, req: Any, route_args: dict, deps: Dependencies,  next_fn: Callable) -> Any:
        return self.handler(req, route_args, deps, next_fn)
