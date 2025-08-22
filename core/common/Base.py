from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, DateTime, func, select, and_, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from core.schemas.base import MSPaginationBaseSchema
from core.common.constants import StatusInvoiceEnum
from math import ceil
from app.common.list_schemas import ListBaseSchema
from core.utils.url import build_url

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_by = Column(String)


class BaseModelInvoice(BaseModel):
    __abstract__ = True
    total_amount = Column(Integer, nullable=False)
    payment_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        Integer, nullable=False, default=StatusInvoiceEnum.UNFINISHED.status_id
    )


class BaseService:
    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db

    async def _save(self, instance):
        try:
            self.db.add(instance)
            await self.db.commit()
            await self.db.refresh(instance)
            return instance
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {str(e.orig)}",
            )
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected server error: {str(e)}",
            )

    async def _delete(self, instance):
        await self.db.delete(instance)
        await self.db.commit()

    async def fetch_one(self, model, **filters):
        try:
            stmt = select(model)
            if filters:
                stmt = stmt.where(
                    and_(
                        *(
                            getattr(model, key) == value
                            for key, value in filters.items()
                        )
                    )
                )
            result = await self.db.execute(stmt)
        except Exception as e:
            raise e
        return result.scalar_one_or_none()

    async def fetch_pagination(
        self,
        stmt,
        data,
        schema_response,
    ):
        prev = None
        next = None
        limit = data["limit"]
        page = data["page"]
        name = data["name"]
        current_url = data["base_url"]
        no_pagination = data["no_pagination"]

        tmp_result = await self.db.execute(stmt)
        tmp_row = tmp_result.all()
        total = len(tmp_row)
        pages = ceil(total / limit) if total else 1
        if no_pagination:
            page = 1

        elif page <= pages:
            cal_offset = (page - 1) * limit
            stmt = stmt.limit(limit).offset(cal_offset)
            parameter_dict = {
                "page": page,
                "limit": limit,
                "no_pagination": no_pagination,
            }
            if page > 1:
                parameter_dict["page"] = page - 1
                prev = build_url(current_url, parameter_dict)
            if page < pages:
                parameter_dict["page"] = page + 1
                next = build_url(current_url, parameter_dict)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )

        item = await self.db.execute(stmt)
        result = item.scalars().all()
        result = [schema_response.from_orm(obj) for obj in result]
        return ListBaseSchema(
            result=result,
            total=total,
            pages=pages,
            page=page,
            limit=limit,
            prev=prev,
            next=next,
        )
