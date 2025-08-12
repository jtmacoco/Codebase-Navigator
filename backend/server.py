from fastapi import FastAPI
from routers import codebase
from fastapi.middleware.cors import CORSMiddleware
from services.codebase_service import CodebaseService
from controllers.codebase_ctrl import CodebaseController
from routers.codebase import codebase_router
from routers.chat import chat_router
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

app.include_router(codebase_router())
app.include_router(chat_router())

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("server:app",reload=True)