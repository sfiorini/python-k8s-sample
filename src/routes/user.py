from typing import List
from fastapi import APIRouter
from models.user import User
from data.users import USERS

router = APIRouter()

@router.get("/user", tags=["Users"], response_model=List[User])
async def list_user():
    return USERS
