# Filesystem crawler and server

### Running this project:

As a Dockerized application, it makes sense to build and run this application quickly, especially so you
don't have to deal with Python version issues. I found one way to do this:

```
docker run -v `pwd`:`pwd` -w `pwd` --rm -p 8080:80 -it $(docker build -q .)
# Credits: https://stackoverflow.com/a/51314059, https://stackoverflow.com/a/76434724

# Then, you can access the API at http://localhost:8080.
curl -i http://localhost:8080

# You can also change the base directory of the application (which must be a subdir of `filesystem_crawler`) using:

export DIR="other_files" && docker run -e UVICORN_BASEDIR=$DIR \
  -v `pwd`:`pwd` \
  -w `pwd` \
  --rm \
  -p 8080:80 \
  -it $(docker build -q .)
```

You can, of course, also run your Docker image however you like.

### Env vars

- UVICORN_BASEDIR: string

### Project notes

My methodology:
- Use the FastAPI `*:path` construction to allow paths to be passed and therefore subdirectories to be rendered.
- I'm using the unix filesystem functions on the `os` module, like `fstat`, to get file information like owner.

### Running tests

- `pip install -r requirements-dev.txt`
- `python -m unittest tests/test_main.py`
