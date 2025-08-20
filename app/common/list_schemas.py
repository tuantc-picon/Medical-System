from typing import Optional, Any
from pydantic import HttpUrl

from core.schemas.base import MSBaseSchema


class ListBaseSchema(MSBaseSchema):
    total: int
    pages: int
    page: int
    limit: int
    prev: Optional[HttpUrl] = None
    next: Optional[HttpUrl] = None
