from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import simulate

app = FastAPI(title="Tactician Pro API", version="0.1.0")

# 允许前端跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(simulate.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)