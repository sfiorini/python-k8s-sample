from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Main"])
async def main():
    return {'message': 'API Server is running successfully'}
