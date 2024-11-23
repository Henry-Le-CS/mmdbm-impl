from flask import request, jsonify
from typing import List, Callable, Any
from werkzeug.exceptions import HTTPException

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
    if isinstance(error, HTTPException):
        response = jsonify({
            "error": str(error),
        })
        
        response.status_code = error.code  # Set the status code from the exception
    else:
        response = jsonify({
            "error": str(error),
        })
        
        response.status_code = 500  # Default to internal server error if it's not an HTTPException

    return response