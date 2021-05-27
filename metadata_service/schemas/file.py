from typing import Optional

from pydantic import BaseModel


class File(BaseModel):
    id: str
    name: Optional[str]
    format: Optional[str]
    type: Optional[str]
    size: Optional[str]
    md5sum: Optional[str]
    category: Optional[str]

