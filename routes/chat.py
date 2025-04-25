from fastapi import APIRouter

router = APIRouter()

@router.get("/next-task")
async def next_task():
    return {"status": "ok"}
