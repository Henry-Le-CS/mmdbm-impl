import os
from src.http import Server, Middleware
from src.http.middlewares import log_request, authenticate, toggle

# API Handlers
from src.api.movies import get_movies, upload_dummy_movies, upload_video

def new_api_registry(s: Server) -> Server:
    s.register_route(
        "/api/movies", 
        get_movies,
        endpoint="get_movies",
        middlewares=[ Middleware(log_request),Middleware(authenticate)],
        methods=["GET"]
    )
    
    s.register_route(
        "/api/rpc/movies/upload-video", 
        upload_video,
        endpoint="upload_video",
        middlewares=[Middleware(log_request),Middleware(authenticate)],
        methods=["POST"],
    )
    
    s.register_route(
        "/api/rpc/movies/upload-dummy-file", 
        upload_dummy_movies,
        endpoint="upload_file",
        middlewares=[
            Middleware(toggle, {
                "toggle": os.getenv("UPLOAD_FILE_API_TOGGLE")
            }),
            Middleware(log_request),
            Middleware(authenticate)],
        methods=["POST"],
    )
   
    return s