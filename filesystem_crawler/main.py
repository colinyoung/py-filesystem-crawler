from fastapi import FastAPI

import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# Setting host and port for application to run on
if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=80)