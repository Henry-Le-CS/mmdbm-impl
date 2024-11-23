from typing import Callable, Any
from src.di.deps import Dependencies

class Middleware:
    def __init__(self, handler: Callable[[Any, dict, Callable], Any], opts: dict = {}) -> None:
        self.handler = handler
        self.opts = opts

    def Exec(self, req: Any, route_args: dict, deps: Dependencies,  next_fn: Callable) -> Any:
        [route_args.update({k: v}) for k, v in self.opts.items()]
        return self.handler(req, route_args, deps, next_fn)
