from app.main import app as fastapi_app


from app.main import app as fastapi_app

import uvicorn

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
