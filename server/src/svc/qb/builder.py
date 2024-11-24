import json
from enum import Enum

class QueryBuilder():
    def __init__(self):
        pass
    
    def build_query_movie_sql(self, opt: dict = {}):
        query = """
            SELECT DISTINCT m.title, m.year, m.ratings, m.url
            FROM movies m
        """
        
        where_conditions = []
        params = {}

        if 'genre' in opt and len(opt['genre']) > 0:
            query += " JOIN movie_genres mg ON m.id = mg.movie_id"
            genre_placeholder = [f":genre{idx+1}" for idx in range(len(opt['genre']))]
            condition = f"mg.genre ILIKE ANY(ARRAY[{', '.join(genre_placeholder)}])"
            where_conditions.append(condition)
            for idx, genre in enumerate(opt['genre']):
                params[f'genre{idx+1}'] = f"%{genre}%"

        if 'actor' in opt and len(opt['actor']) > 0:
            query += " JOIN movie_actors ma ON m.id = ma.movie_id"
            query += " JOIN actors a ON ma.actor_id = a.id"
            actor_placeholder = [f":actor{idx}" for idx in range(len(opt['actor']))]
            condition = f"a.name ILIKE ANY(ARRAY[{', '.join(actor_placeholder)}])"
            where_conditions.append(condition)
            for idx, actor in enumerate(opt['actor']):
                params[f'actor{idx}'] = f"%{actor}%"

        if 'title' in opt and len(opt['title']) > 0:
            title_placeholder = [f":title{idx}" for idx in range(len(opt['title']))]
            condition = f"m.title ILIKE ANY(ARRAY[{', '.join(title_placeholder)}])"
            where_conditions.append(condition)
            for idx, title in enumerate(opt['title']):
                params[f'title{idx}'] = f"%{title}%"
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        
        # Return the query and the dictionary of parameters
        return query, params

    def build_task_management_sql(self, job_id: str, status: str | Enum, args: dict = None, result: dict = None):
        if not job_id:
            raise ValueError("job_id is required")
        if not status:
            raise ValueError("status is required")
        
        if isinstance(status, Enum):
            status = status.value
        
        params = {
            "job_id": job_id,
            "status": status
        }
        
        insert_part = """INSERT INTO tasks VALUES (:job_id, :status"""
        conflict_part = " ON CONFLICT (job_id) DO UPDATE SET status = :status"
        if args:
            insert_part += ", :args"
            conflict_part += ", args = :args"
            params["args"] = json.dumps(args)

        if result:
            insert_part += ", :result"
            conflict_part += ", result = :result"
            params["result"] = json.dumps(result)

        return insert_part + ")" + conflict_part + ";", params
            