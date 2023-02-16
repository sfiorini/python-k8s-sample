from typing import List
from fastapi import APIRouter
from models.user import User
from data.users import USERS
from utils.exceptions import CustomException

# Return current array index of user or abort if user does not exist.
def user_exist(user_email):
    index = next((i for i, item in enumerate(USERS)
                 if item['email'] == user_email), -1)
    if (index < 0):
        raise CustomException(code=404, message="User email {} doesn't exist".format(user_email))
    
    return index

router = APIRouter()

@router.get("/user", tags=["Users"], response_model=List[User])
async def list_users():
    return USERS


@router.get("/user/{email}", tags=["Users"], response_model=User)
async def get_user(email: str):
    index = user_exist(email)
    return USERS[index]