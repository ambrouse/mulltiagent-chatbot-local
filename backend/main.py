from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from router.router import api_router
from database.setup_postgres import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield 

# 1. Khởi tạo Fast
app = FastAPI(
    title="My FastAPI Backend",
    description="Backend cho project",
    version="1.0.0",
    lifespan=lifespan
)

# 2. (CORS)
origins = [
    "http://localhost:9002", # Port mặc định của React
    "http://127.0.0.1:9002",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], # Cho phép tất cả các method (GET, POST, PUT, DELETE...)
    allow_headers=["*"], # Cho phép tất cả các headers
)
app.include_router(api_router, prefix="/api/v1") # Gắn toàn bộ hệ thống router vào app

print("="*50+"\n")
print("- Backend running...")
print("\n"+"="*50)

# 3. Chạy server 
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)