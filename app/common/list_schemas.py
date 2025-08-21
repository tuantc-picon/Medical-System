from typing import Optional, Generic, TypeVar, List

from core.schemas.base import MSBaseSchema

DataT = TypeVar("DataT")


class ListBaseSchema(MSBaseSchema, Generic[DataT]):
    total: int
    pages: int
    page: int
    limit: int
    prev: Optional[str] = None
    next: Optional[str] = None
    result: List[DataT]
