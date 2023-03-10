from typing import Optional

from pydantic import BaseModel, Field

class User(BaseModel):
    email: Optional[str] = Field(nullable=True)
    firstName: Optional[str] = Field(nullable=True)
    lastName: Optional[str] = Field(nullable=True)
    
    class Config:
        orm_mode = True
