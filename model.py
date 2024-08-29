from pydantic import BaseModel
from typing import List

class Article(BaseModel):
    title: str
    body: str
    url: str
    tags: List[str]

