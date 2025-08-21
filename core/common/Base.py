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
from app.users.schemas.user import UserReadSchema

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
        pagination_data: MSPaginationBaseSchema,
        current_url,
        total_user,
        schema_response,
    ):
        pages = ceil(total_user / pagination_data.limit_page) if total_user else 1

        prev = None
        next = None

        if pagination_data.no_pagination:
            pagination_data.page = 1
            pagination_data.limit_page = total_user

        elif pagination_data.page <= pages:
            cal_offset = (pagination_data.page - 1) * pagination_data.limit_page
            stmt = stmt.offset(cal_offset)
            stmt = stmt.limit(pagination_data.limit_page)
            if pagination_data.page > 1:
                prev = f"{current_url}?page={pagination_data.page-1}&limit={pagination_data.limit_page}&no_pagination=false"
            if pagination_data.page < pages:
                next = f"{current_url}?page={pagination_data.page+1}&limit={pagination_data.limit_page}&no_pagination=false"

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )

        item = await self.db.execute(stmt)
        result = item.scalars().all()
        return ListBaseSchema[schema_response](
            result=result,
            total=total_user,
            pages=pages,
            page=pagination_data.page,
            limit=pagination_data.limit_page,
            prev=prev,
            next=next,
        )
