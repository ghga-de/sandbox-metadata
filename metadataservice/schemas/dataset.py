from typing import List, Optional

from pydantic import BaseModel


class Dataset(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    files: Optional[List[str]] = None
    has_study: Optional[str] = None
