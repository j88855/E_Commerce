from pydantic import BaseModel, EmailStr,  Field, StringConstraints, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(min_length=2, max_length=20)] = Field(..., description="使用者姓名, 2~20字")
    email: Annotated[EmailStr, StringConstraints(min_length=5, max_length=50)] = Field(..., description="電子郵件")
    password: Annotated[str, StringConstraints(min_length=8, max_length=20)] = Field(..., description="密碼, 8~20字")

class UserLogin(BaseModel):
    username: Annotated[str, StringConstraints(min_length=2, max_length=20)] = Field(..., description="使用者姓名, 2~20字")
    password: Annotated[str, StringConstraints(min_length=8, max_length=20)] = Field(..., description="密碼, 8~20字")

class UserUpdate(BaseModel):
    username: Optional[Annotated[str, StringConstraints(min_length=2, max_length=20)]]  = Field(default=None, description="使用者姓名, 2~20字")
    email: Optional[Annotated[EmailStr, StringConstraints(min_length=5, max_length=50)]] = Field(default=None, description="電子郵件")
    password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=20)]] = Field(default=None, description="密碼, 8~20字")

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AdminUserOut(UserOut):
    role: str