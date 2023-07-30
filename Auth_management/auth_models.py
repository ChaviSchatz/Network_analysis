from typing import Union

from pydantic import BaseModel, constr, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[EmailStr, None] = None


class User(BaseModel):
    password: Union[constr(min_length=8), None] = None
    disabled: Union[bool, None] = None
    email: Union[EmailStr, None] = None
    full_name: Union[constr(max_length=40), None] = None
