import logging
import time
from flask import request
from werkzeug.exceptions import NotFound

# If this is toggle off, the api will return 404
def toggle(req, route_args, deps, next_fn):
    t = route_args.get("toggle")
    if t is not None and t == "off":
        logging.info(f"[{time.time()}] {request.method} {request.path} - Toggle off")
        raise NotFound("API is disabled")
    
    return next_fn()