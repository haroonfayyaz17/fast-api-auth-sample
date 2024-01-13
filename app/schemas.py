import re
from pydantic import BaseModel, validator, Field
from typing import Optional


class User(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=99)
    email: str = Field(
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    password: str = Field(min_length=8, max_length=20,
                          description="Password must contain at least one letter, one digit, and can include @$!%*?&")

    @validator("password")
    def validate_password(cls, password, **kwargs):
        # Put your validations here
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
        if (re.match(pattern, password)):
            return password
        else:
            raise ValueError(
                'Password should contain at least one uppercase letter, one lowercase letter, one special character, and one number')


class UserLogin(BaseModel):
    email: str
    password: str
