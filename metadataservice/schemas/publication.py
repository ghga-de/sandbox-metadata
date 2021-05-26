from typing import Optional

from pydantic import BaseModel


class Publication(BaseModel):
    id: str
    title: Optional[str] = None
