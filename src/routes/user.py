from typing import List
from fastapi import APIRouter
from models.user import User
from data.users import USERS
from utils.exceptions import CustomException

# Return current array index of user or -1 if user does not exist.
def user_exist(user_email):
    index = next((i for i, item in enumerate(USERS)
                    if item['email'] == user_email), -1)
    return index


router = APIRouter()


@router.post("/user", tags=["Users"], response_model=List[User], status_code=201)
async def create_user(user: User):
    if (not user.email):
        raise CustomException(
            code=422, message="User email is a required field")
    index = user_exist(user.email)
    if (index >= 0):
        raise CustomException(
            code=409, message="User email {} already exist".format(user.email))
    USERS.append(user)
    return USERS


@router.get("/user", tags=["Users"], response_model=List[User])
async def list_users():
    return USERS


@router.get("/user/{email}", tags=["Users"], response_model=User)
async def get_user(email: str):
    index = user_exist(email)
    if (index < 0):
        raise CustomException(
            code=404, message="User email {} doesn't exist".format(email))

    return USERS[index]


@router.put("/user/{email}", tags=["Users"], response_model=User, status_code=201)
async def edit_user(email: str, updatedUser: User):
    index = user_exist(email)
    if (index < 0):
        raise CustomException(
            code=404, message="User email {} doesn't exist".format(email))
    newEmail = updatedUser.email
    newFirstName = updatedUser.firstName
    newLastName = updatedUser.lastName
    if (newEmail and newEmail != email):
        newEmailIndex = user_exist(newEmail)
        if (newEmailIndex >= 0):
            raise CustomException(
                code=409, message="New User email {} already exist".format(newEmail))
        USERS[index]['email'] = newEmail
    if (newFirstName):
        USERS[index]['firstName'] = newFirstName
    if (newLastName):
        USERS[index]['lastName'] = newLastName
    return USERS[index]


@router.delete("/user/{email}", tags=["Users"], status_code=204)
async def delete_user(email: str):
    index = user_exist(email)
    if (index < 0):
        raise CustomException(
            code=404, message="User email {} doesn't exist".format(email))

    del USERS[index]
    return None
