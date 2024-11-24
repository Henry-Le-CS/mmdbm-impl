import os
from src.http import Server, Middleware
from src.http.middlewares import log_request, authenticate, toggle

# API Handlers
from src.api.movies import list_movies, upload_dummy_movies, upload_video
from src.api.tasks import list_tasks

def new_api_registry(s: Server) -> Server:
    return s.register_route(
        "/api/movies", 
        list_movies,
        endpoint="get_movies",
        middlewares=[Middleware(log_request),Middleware(authenticate)],
        methods=["GET"]
    ).register_route(
        "/api/rpc/movies/upload-video", 
        upload_video,
        endpoint="upload_video",
        middlewares=[Middleware(log_request),Middleware(authenticate)],
        methods=["POST"],
    ).register_route(
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
    ).register_route(
        "/api/tasks", 
        list_tasks,
        endpoint="list_tasks",
        middlewares=[Middleware(log_request),Middleware(authenticate)],
        methods=["GET"]
    )