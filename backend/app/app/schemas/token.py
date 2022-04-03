from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class Face(BaseModel):
    name: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
