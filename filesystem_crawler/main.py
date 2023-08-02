import os

from fastapi import FastAPI, Response
import uvicorn

from .result import Result
from .input import Input

app = FastAPI()

# Basedir defaults to UVICORN_BASEDIR environment variable, which is case sensitive.
default_path = "files"
envdir = os.environ.get("UVICORN_BASEDIR", default_path)
if envdir == ".":
    raise ValueError("Cannot use current directory as basedir")

basedir = os.path.join(os.path.dirname(__file__),
                       envdir)

print(f"Starting filesystem crawler in {basedir}.")

def index_of(path, response):
    try:
        results = []
        for entry in os.scandir(path):
            results.append(Result(entry=entry))
        return results
    except PermissionError:
        response.status_code = 403
        return {"error": "Permission denied"}
    except FileNotFoundError:
        response.status_code = 404
        return {"error": "File not found"}
    except NotADirectoryError:
        response.status_code = 400
        return {"error": "Not a directory"}


def contents_of(result: Result, response: Response):
    try:
        contents = result.file_contents()
        return {"name": result.name, "contents": contents}
    except PermissionError:
        response.status_code = 403
        return {"error": "Permission denied"}
    except IsADirectoryError:
        response.status_code = 400
        return {"error": "Cannot read a directory"}


def upsert_file(input: Input, path: str):
    try:
        input.save(path)
    except Exception as e:
        raise e

@app.get("/")
async def root_dir(response: Response) -> list[Result]:
    return index_of(basedir, response)

# List contents of any directory - must be subdir of basedir
# I'd prefer this was just the same method as above with an optional path parameter,
# but I need Response to be passed in to set the status code


@app.get("/{path:path}") # https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor
async def get_file_or_directory_at_path(path: str, response: Response) -> list[Result]:
    safe_path = os.path.join(basedir, path)
    try:
        result = Result(path=safe_path)
        if result.type == "file":
            return contents_of(result, response)

    except FileNotFoundError:
        response.status_code = 404
        return {"error": "File not found"}

@app.post("/{path:path}")
async def upsert_file_or_directory_at_path(input: Input, path: str, response: Response) -> list[Result]:
    try:
        dir = Result(path=basedir)
        if dir.type != "directory":
            response.status_code = 400
            return {"error": "Not a valid directory for file"}
        
        safe_path = os.path.join(basedir, path)
        result = upsert_file(input, safe_path)
        if result == None:
            # directory created
            response.status_code = 200 # No Content
            return { "status" : f"Directory now exists at {path}" }
        return { "contents" : result }
    except Exception as e:
        response.status_code = 400
        return {"error": e.__str__()}


# Setting host and port for application to run on
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
