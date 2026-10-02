from fastapi import APIRouter


router = APIRouter(
    prefix="/tools",
    tags=["Tools"],
)


@router.get("/")
def list_tools():

    return {
        "tools": [
            "database",
            "payment",
            "email",
        ]
    }