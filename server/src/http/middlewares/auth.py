from src.http.middleware import Middleware

def authenticate(req, route_args, deps, next_fn):
    # TODO: Implement authentication logic here
    return next_fn()