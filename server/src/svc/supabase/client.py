import logging
from supabase import create_client, Client

class SupabaseClient:
    def __init__(
        self, 
        url, 
        key,
        bucket_name: str = "public"
    ):
        self._url = url
        self._api_key = key
        self._bucket_name = bucket_name
        self._init_client()
        logging.info("SupabaseClient initialized")
        
    def _init_client(self):
        self._client = create_client(self._url, self._api_key)
        
    def upload_file(
        self, 
        file_path: str, 
        content_type: str = "text/plain;charset=UTF-8",
        allow_overwrite: bool = False
    ):
        try:
            with open(file_path, "rb") as f:
                filename = file_path.split("/")[-1]
                response = self._client.storage \
                    .from_(self._bucket_name) \
                    .upload(
                        file=f,
                        path=filename, # just upload the file, we do not support subfolders now
                        file_options={
                            "cache-control": "3600", 
                            "upsert": "false" if not allow_overwrite else "true",
                            "content-type": content_type       
                        },
                    )
                    
                return response
        except Exception as e:
            logging.warning(f"Error uploading file: {e}")
            raise e