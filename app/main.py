from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes.agent import router as agent_router
from app.api.routes.health import router as health_router
from app.api.routes.tools import router as tools_router
from app.api.routes.approval import router as approval_router


BASE_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_FILE = BASE_DIR / "dashboard" / "index.html"


app = FastAPI(
    title="AI Agent Guard",
    description="Security and authorization gateway for AI agents",
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(agent_router, prefix="/v1")
app.include_router(tools_router, prefix="/v1")
app.include_router(approval_router, prefix="/v1")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(DASHBOARD_FILE)


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(DASHBOARD_FILE)