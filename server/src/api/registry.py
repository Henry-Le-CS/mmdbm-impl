from src.http import Server, Middleware
from src.http.middlewares import log_request, authenticate

# API Handlers
from src.api.movies import get_movies

def new_api_registry(s: Server) -> Server:
    s.register_route(
        "/api/movies", 
        get_movies,
        middlewares=[Middleware(log_request),Middleware(authenticate)],
        methods=["GET"]
    )
    
    return s