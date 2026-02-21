from pydantic import BaseModel
from typing import List, Dict


class LinkedInPost(BaseModel):
    content: str
    scores: Dict[str, int]


class TwitterThread(BaseModel):
    tweets: List[str]
    scores: Dict[str, int]