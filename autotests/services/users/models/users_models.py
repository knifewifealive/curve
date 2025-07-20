from pydantic import BaseModel, Field
from typing import List, Literal, Union



class InformationGetSchema(BaseModel):
    id: int
    information: str
    explanation: str
    repeat_date_1: str
    repeat_date_2: str
    repeat_date_3: str
    repeat_date_4: str
    repeat_date_5: str
    user_nickname: str

class InformationPostSchema(BaseModel):
    information: str = Field(min_length=1, max_length=30)
    explanation: str = Field(min_length=1, max_length=200)

class StatusSchema(BaseModel):
    status: Literal['success']

class UserGetSchema(BaseModel):
    nickname: str
    first_name: str
    last_name: str
    age: int
    job: str

class UserPostSchema(BaseModel):
    nickname: str = Field(min_length=1, max_length=20)
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=20)
    age: int = Field(ge=1, le=99)
    job: str = Field(min_length=1, max_length=100)

class UserPutSchema(BaseModel):
    age: int = Field(ge=1, le=99)
    job: str = Field(min_length=1, max_length=100)

class UserValidationError(BaseModel):
    loc: List[Union[int,str]]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: List[UserValidationError]
