from typing import Union

from pydantic import BaseModel, constr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    password: Union[constr(min_length=8), None] = None
    disabled: Union[bool, None] = None
    user_name: constr(min_length=3, max_length=20)
    full_name: constr(max_length=40)
