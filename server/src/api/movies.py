import os
from flask import request
from src.di.deps import Dependencies

def get_movies(req, route_args, deps: Dependencies):
    q = request.args.get("q")
    if q is None:
        raise Exception("Missing query parameter 'q'")

    entities = deps.get_detector().explore(q)
    opt = dict()
    for ent in entities:
        if opt.get(ent[1]) is None:
            opt[ent[1]] = []
        
        opt[ent[1]] = opt[ent[1]] + [ent[0]]

    q, params = deps \
                .get_qb() \
                .build_query_movie_sql(opt=opt)

    m = []
    for row in deps.get_db().query(q, params):
        m.append({
            "title": row[0],
            "year": row[1],
            "ratings": row[2]
        })

    return {
        "movies": m,
    }

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
        return str(e)