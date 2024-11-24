from flask import request
from src.di import Dependencies
from werkzeug.exceptions import BadRequest, InternalServerError

def list_tasks(req, route_args, deps: Dependencies):
    offset = int(request.args.get("offset") or 0)
    limit = int(request.args.get("limit") or 10)
    if offset < 0 or limit < 0:
        raise BadRequest("Invalid offset or limit")
    
    orderBy = "created_at DESC"
    if request.args.get("orderBy") == "oldest":
        orderBy = "created_at ASC"
    
    try:
        data = deps.get_db().query("""
            SELECT job_id, status, result, created_at 
            FROM tasks
            ORDER BY """ + orderBy, {
        })
        
        ret = [
            {
                "job_id": d[0],
                "status": d[1],
                "result": {
                        "movie_id": d[2].get("movie_id"),
                        "full_path": d[2].get("full_path")
                    } if d[2] != {} else None,
                "created_at": d[3]
            } for d in data[offset:offset+limit] 
            # Pagin on mem, we can use OFFSET and LIMIT in SQL if we have another index to reduce dimension
        ]
        
        return {
            "tasks": ret,
            "hasMore": len(data) > offset + limit
        }
    except Exception as e:
        raise InternalServerError(str(e))
        
    