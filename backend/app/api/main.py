from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import jd, ranking, report, stats

app = FastAPI(title="Recruiter Copilot API", version="0.1.0")

# Local React dev servers (CRA on 3000, Vite on 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jd.router, prefix="/api")
app.include_router(ranking.router, prefix="/api")
app.include_router(report.router, prefix="/api")
app.include_router(stats.router, prefix="/api")


@app.get("/api/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}
