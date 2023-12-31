FROM python:3.10-alpine
WORKDIR /wg-takehome

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

# This is where you can set the default subdirectory to render files of.
ENV uvicorn_basedir files

# Feel free to swap out this command if you do not want to use FastAPI
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "filesystem_crawler.main:app"]
