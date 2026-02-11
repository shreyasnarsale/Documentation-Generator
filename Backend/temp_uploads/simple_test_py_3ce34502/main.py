from fastapi import FastAPI
from routes import router

app = FastAPI(title="Simple Test Project")
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello from Simple Test Project"}