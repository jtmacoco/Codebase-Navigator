from fastapi import FastAPI
from routers import codebase
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
origins = [
    "http://localhost:3000"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(codebase.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("server:app",reload=True)