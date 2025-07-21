from typing import Any, List, Optional, Union

from pydantic import BaseModel, ConfigDict


from datetime import datetime, date
from typing import Annotated, Optional
from typing import Union, Any, Dict
from zoneinfo import ZoneInfo

from fastapi import Query
from pydantic import BaseModel
from pydantic import GetJsonSchemaHandler
from pydantic_core import CoreSchema
from pydantic_core.core_schema import ValidationInfo

from config import DEFAULT_TIMEZONE_SERVER
from core.common.constants import SortType


# class MSBaseSchema(BaseModel):
#     pass

class MSPaginationBaseSchema(BaseModel):
    page: Annotated[int, Query(ge=1)] = 1
    limit: Annotated[int, Query(ge=1, le=1000)] = 20
    no_pagination: Optional[Annotated[bool, Query()]] = False


class MSSortBaseSchema(BaseModel):
    sort_by: Optional[Annotated[str, Query()]] = None
    sort_type: Optional[Annotated[int, Query()]] = SortType.ASC


class MSSortPaginationBaseSchema(
    MSSortBaseSchema, MSPaginationBaseSchema
):
    pass


class MSTimestamp:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(
        cls, value: Union[int, datetime], info: ValidationInfo
    ) -> datetime | int | None:
        if value is None:
            return value

        from_attributes = info.config.get("from_attributes")
        if from_attributes:
            return cls.__pre_from_orm(value)
        else:
            return cls.__pre_commit(value)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> Dict[str, Any]:
        return {
            "type": "integer",
            "example": 1629264000,
            "format": "timestamp",
            "description": "An integer timestamp that can be converted to a datetime object.",
        }

    @classmethod
    def __pre_commit(cls, value: Union[int, datetime]) -> datetime:
        if isinstance(value, int):  # If the input is epoch time
            if len(str(value)) > 13:
                raise ValueError(
                    "Invalid timestamp value. Must be an integer (epoch time) or a datetime object."
                )
            if len(str(value)) > 10:
                return datetime.fromtimestamp(
                    value / 1000, tz=ZoneInfo(DEFAULT_TIMEZONE_SERVER)
                )

            return datetime.fromtimestamp(value, tz=ZoneInfo(DEFAULT_TIMEZONE_SERVER))
        elif isinstance(value, datetime):
            return value
        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        raise ValueError(
            "Invalid timestamp value. Must be an integer (epoch time) or a datetime object."
        )

    @classmethod
    def __pre_from_orm(cls, value: Union[int, datetime]) -> int:
        if isinstance(value, datetime):
            return cls.to_epoch(value)
        elif isinstance(value, int):
            return value

        raise ValueError(
            "Invalid timestamp value. Must be an integer (epoch time) or a datetime object."
        )

    @classmethod
    def to_epoch(cls, value: datetime) -> int:
        return int(value.timestamp() * 1000)  # Returns epoch in milliseconds

    def __repr__(self):
        return f"Timestamp({self.to_epoch(self)})"


class MSBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def __init__(
        self, items: Union[Any, List[Any]], many: Optional[bool] = False, **kwargs
    ):
        if many:
            schema_data = [self.__class__.from_orm(item).dict() for item in items]
            object.__setattr__(self, "__dict__", {"items": schema_data})
        else:
            if hasattr(items, "__dict__"):
                schema_data = self.from_orm(items).dict()
                object.__setattr__(self, "__dict__", schema_data)
            else:
                object.__setattr__(self, "__dict__", items)
                super().__init__(**kwargs)

    @property
    def data(self):
        return self.dict()

    def dict(self, *args, **kwargs):
        if hasattr(self, "items"):
            return getattr(self, "items")
        return super().dict(*args, **kwargs)
