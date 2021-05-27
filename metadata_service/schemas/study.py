from typing import List, Optional

from pydantic import BaseModel


class Study(BaseModel):
    id: str
    title: Optional[str] = None
    type: Optional[str] = None
    abstract: Optional[str] = None
    publications: Optional[List[str]] = None
