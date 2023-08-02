import os

from fastapi import FastAPI, Response
import uvicorn

from .result import Result

app = FastAPI()

# Basedir defaults to UVICORN_BASEDIR environment variable, which is case sensitive.
default_path = "files"
basedir = os.path.join(os.path.dirname(__file__),
                       os.environ.get("UVICORN_BASEDIR", default_path))

print(f"Starting filesystem crawler in {basedir}.")


def index_of(path, response):
    try:
        results = []
        print(path)
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

# List contents of root directory
# I'd prefer to have this


@app.get("/")
async def root(response: Response) -> list[Result]:
    return index_of(basedir, response)

# List contents of any directory - must be subdir of basedir
# I'd prefer this was just the same method as above with an optional path parameter,
# but I need Response to be passed in to set the status code


@app.get("/{path:path}") # https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor
async def path_index(path: str, response: Response) -> list[Result]:
    safe_path = os.path.join(basedir, path)
    try:
        result = Result(path=safe_path)
        if result.type == "file":
            return contents_of(result, response)

        return index_of(safe_path, response)
    except FileNotFoundError:
        response.status_code = 404
        return {"error": "File not found"}


# Setting host and port for application to run on
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
