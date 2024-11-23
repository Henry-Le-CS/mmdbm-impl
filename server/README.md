# Server Implementation

This folder contains server implementation for a multimedia database management system

In this repo, there are 2 main entities: **Server** and **Worker**.

- Server: This is where the API will be handled and forward to worker
- Worker: Resolve heavy jobs such as file uploading to supabase

## How to run:

Before running, you need to make sure that you are having 2 datab instances: **Postgres** and **Redis**

This is because the worker will be backed by **Redis**.
Also, you may need to have Supabase Key and URL to be able to upload files there.

All the configs can be seen in .env.example:

### Prepare environment:
In the CWD, run the following to prepare virtual environment and download dependencies
```bash
    cd server && python -m venv venv
```

For MacOS, run:
```bash
    source venv/bin/activate && pip install -r requirements.txt
```

For Windows cmd.exe, run:
```bash
    C:\> venv\Scripts\activate.bat && pip install -r requirements.txt
```

For Windows PowerShell, run:
```bash
    PS C:\> venv\Scripts\Activate.ps1 && pip install -r requirements.txt
```

You can reference to this at https://docs.python.org/3/library/venv.html#how-venvs-work

### Start server

Once the dependencies, databases are set up, we are ready to start the server. In the server folder, run:

```bash
    python3 main.py
```

Then the server is ready to receive APIs

### Start the worker
Similarly, you also need to start the worker. In the server folder, run:
```bash
    celery -A worker.app worker --loglevel=INFO
```

## APIs

The APIs are still developed. But you can mock some data and try it on your own.

* Get a movie list based on query:
```bash
    curl --location '{{host}}/api/movies?q=the%20romance%20genre'
```

* Upload a movie to database:
```bash
curl --location 'http://localhost:3001/api/rpc/movies/upload-video' \
--form 'file=@"root/to/your/video/or/files"' \
--form 'title="It is working lol"' \
--form 'year="1012"' \
--form 'genres="[\"romance\",\"thriller\"]"' \
--form 'actors="[\"A\",\"B\", \"C\"]"' \
--form 'ratings="10"'
```
