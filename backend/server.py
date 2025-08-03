from fastapi import FastAPI
from routers import codebase
import uvicorn
app = FastAPI()
app.include_router(codebase.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("server:app",reload=True)