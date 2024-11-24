import os
from enum import Enum
from httpx import Response
from src.svc.worker.task_registry import TaskRegistry


class Progress(Enum):
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    COMPLETED = "completed"

def upload_files(
    job_id: str,
    localFilePath: str,
    content_type: str,
    metadata: dict = {},
):
    # Import from here prevent process forking crash. I am not sure why this is happening for now
    # ref: https://stackoverflow.com/a/65547214/23303968
    from src.di import Dependencies
    from src.db import Database
    from src.svc import SupabaseClient, StorageService,QueryBuilder
    
    # TODO: implemen singleton pattern here
    # Must try some dependency injection here because this is not efficient            
    d = Dependencies(
        storage_svc=StorageService(),
        sbc=SupabaseClient(
            url=os.getenv("SUPABASE_URL"),
            key=os.getenv("SUPABASE_KEY"),
            bucket_name=os.getenv("SUPABASE_BUCKET_NAME")
        ),
        db=Database(uri=os.getenv("DATABASE_URI")),
        qb=QueryBuilder()
    )
    is_status_updated = False
    try:        
        r: Response = d.get_sbc().upload_file(localFilePath, content_type)
        # TODO: start transaction
        insert_result = d.get_db().execute(
            "INSERT INTO public.movies (title, year, ratings, url) VALUES (:title, :year, :ratings, :url) RETURNING id;",
            {
                "title": metadata.get("title"),
                "year": metadata.get("year"),
                "ratings": metadata.get("ratings"),
                "url": r.full_path
            }
        )

        [row_id] = insert_result
        row_id = row_id[0]
        if row_id is None:
            raise Exception("Error inserting movie")
        
        if metadata.get("genres"):
            for genre in metadata.get("genres"):
                d.get_db().execute(
                    "INSERT INTO movie_genres (movie_id, genre) VALUES (:movie_id, :genre) ON CONFLICT DO NOTHING",
                    {
                        "movie_id": row_id,
                        "genre": genre
                    }
                )

        if metadata.get("actors"):
            for actor in metadata.get("actors"):
                d.get_db().execute(
                    "INSERT INTO movie_actors (movie_id, actor_name) VALUES (:movie_id, :actor_name) ON CONFLICT DO NOTHING",
                    {
                        "movie_id": row_id,
                        "actor_name": actor
                    }
                )
        q, params = d.get_qb().build_task_management_sql(job_id, Progress.COMPLETED, None, 
            result = {
            "outcome": Progress.COMPLETED.value,
            "movie_id": row_id,
            "full_path": r.full_path
            })
        d.get_db().execute(q, params)
        is_status_updated = True
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "url": r.full_path
        }
        
    except Exception as e: 
        q, params = d.get_qb().build_task_management_sql(job_id, Progress.FAILED, None, result = {
            "outcome":  Progress.FAILED.value,
            "message": str(e)
        })       
        d.get_db().execute(q, params)
        is_status_updated = True
        raise e
    finally:
        d.get_storage_svc().remove_file(localFilePath)
        if not is_status_updated:
            q, params = d.get_qb().build_task_management_sql(job_id, Progress.FAILED, None, result = {
                "outcome": Progress.FAILED.value,
                "message": "Error uploading file"
            })
            # Marked as failed if the status is not updated        
            d.get_db().execute(q, params)
        

def register_tasks(task_registry: TaskRegistry) -> TaskRegistry:
    task_registry.register("upload_files", upload_files)
    return task_registry