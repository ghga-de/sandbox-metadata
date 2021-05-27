from typing import Optional

from pydantic import BaseModel


class Experiment(BaseModel):
    id: str
    name: Optional[str] = None
    has_study: Optional[str] = None
    instrument_model: Optional[str] = None
