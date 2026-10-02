from fastapi import APIRouter


router = APIRouter(
    prefix="/approval",
    tags=["Approval"],
)


@router.get("/")
def approval_status():

    return {
        "status": "approval_service_ready",
        "message": "Human approval workflow will be implemented next.",
    }