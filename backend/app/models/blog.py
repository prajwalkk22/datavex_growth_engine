from pydantic import BaseModel
from typing import Dict, List


class BlogDraft(BaseModel):
    content: str
    scores: Dict[str, int]


class BlogEvolution(BaseModel):
    draft_number: int
    scores: Dict[str, int]
    key_changes_made: List[str]