import os
import json
from flask import request
from src.di.deps import Dependencies
from src.svc import Progress
from werkzeug.exceptions import BadRequest

def list_movies(req, route_args, deps: Dependencies):
    q = request.args.get("q")
    if q is None:
        raise Exception("Missing query parameter 'q'")

    entities = deps.get_detector().explore(q)
    opt = dict()
    [opt.setdefault(ent[1], []).append(ent[0]) for ent in entities]

    q, params = deps.get_qb() \
                .build_query_movie_sql(opt=opt)

    m = [
        {
            "title": row[0],
            "year": row[1],
            "ratings": row[2],
            "url": row[3],
            "id": row[4]
        } for row in deps.get_db().query(q, params)
    ]
    return {
        "movies": m,
    }
    
def upload_video(req, route_args, deps: Dependencies):
    if 'file' not in request.files:
        raise BadRequest("No file part")
    
    file = request.files['file']
    if file.filename == '':
        raise BadRequest("No selected file")
    
    # extract movie title, year, and genres, actors, ratings from the request body
    title = request.form.get("title")
    year = request.form.get("year")
    genres = request.form.get("genres")
    actors = request.form.get("actors")
    ratings = request.form.get("ratings")
    if title is None or year is None or genres is None or actors is None or ratings is None or len(genres) == 0 or len(actors) == 0:
        raise BadRequest("Missing required fields")
    
    genres = json.loads(genres)
    actors = json.loads(actors)
    
    try:
        metadata = deps.get_storage_svc().save_file(file)
        args = [
            metadata.get("storage_path"),
            file.content_type,
            {
                "title": title,
                "year": year,
                "genres": genres,
                "actors": actors,
                "ratings": ratings
            }
        ]
        
        job_id = deps.get_task_enqueuer().enqueue_task("upload_files", args=args)
        q, params = deps.get_qb().build_task_management_sql(job_id, Progress.IN_PROGRESS, args=args)
        deps.get_db().execute(q, params)
        return {
            "message": Progress.IN_PROGRESS.value,
            "job_id": job_id
        }

    except Exception as e:
        raise e

# Only use for testing
def upload_dummy_movies(req, route_args, deps: Dependencies):
    try:
        file_path = os.getcwd() + '/assets/test_image.jpg'
        r = deps.get_sbc().upload_file(
            file_path=file_path,
            content_type="image/jpeg",
            allow_overwrite=True
        )
        
        return r
    except Exception as e:
        raise e