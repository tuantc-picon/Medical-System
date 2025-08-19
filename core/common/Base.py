from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, DateTime, func, select, and_, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from core.schemas.base import MSPaginationBaseSchema
from core.common.constants import StatusInvoiceEnum

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
        pagination_data=MSPaginationBaseSchema,
    ):
        if pagination_data.no_pagination:
            result = await self.db.execute(stmt)
            return result.scalars().all()

        stmt = stmt.limit(pagination_data.limit)
        offset = (pagination_data.page - 1) * pagination_data.limit
        stmt = stmt.offset(offset)
        try:
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise e
