# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import simulate

app = FastAPI(title="Tactician Pro Backend")

# ================= CORS 配置 =================
# 允许前端 Vite 默认端口访问
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ============================================

# 注册路由
app.include_router(simulate.router, prefix="/api")