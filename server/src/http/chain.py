from flask import request
from typing import List, Callable, Any

from src.http.middleware import Middleware
from src.di.deps import Dependencies

def Chain(deps: Dependencies, middlewares: List[Middleware], api_handler:  Callable[..., Any]) -> Callable[..., Any]:
    def chained_handler(*args: Any, **kwargs: Any) -> Any:
        def next_middleware(index: int) -> Any:
            if index < len(middlewares):
                return middlewares[index].Exec(args, kwargs, deps, lambda: next_middleware(index + 1))
            
            # Finished all middlewares, call the API handler
            return api_handler(args, kwargs, deps)

        try:
            return wrapSuccess(next_middleware(0))
        except Exception as e:
            return wrapError(e)

    return chained_handler

def wrapSuccess(data):
    return {
        "data": data
    }
    
def wrapError(error):
    return {
        "error": str(error)
    }