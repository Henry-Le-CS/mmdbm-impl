import logging
import time
from flask import request
from src.http.middleware import Middleware

def log_request(req, route_args, deps, next_fn):
    logging.info(f"[{time.time()}] {request.method} {request.path}")
    return next_fn()