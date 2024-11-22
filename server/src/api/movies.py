from flask import request
from src.di.deps import Dependencies
def get_movies(req, route_args, deps: Dependencies):
    q = request.args.get("q")
    e = deps.get_detector().explore(q)
    return {
        "parsed_query": q,
        "movies": e
    }