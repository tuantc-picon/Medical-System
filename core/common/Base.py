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
        model,
        conditions,
        user_dict,
        schema_response,
    ):
        prev = None
        next = None
        limit = user_dict["limit"]
        page = user_dict["page"]
        name = user_dict["name"]
        role_id = user_dict["role_id"]
        current_url = user_dict["base_url"]
        no_pagination = user_dict["no_pagination"]

        total_stm = select(func.count()).select_from(model).where(*conditions)
        total_user = await self.db.scalar(total_stm)

        pages = ceil(total_user / limit) if total_user else 1
        stmt = select(model).where(*conditions)
        if no_pagination:
            page = 1

        elif page <= pages:
            cal_offset = (page - 1) * limit
            stmt = stmt.offset(cal_offset)
            stmt = stmt.limit(limit)
            parameter_dict = {
                "page": page,
                "limit": limit,
                "no_pagination": no_pagination,
                "role_id": role_id,
                "name": name,
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
            total=total_user,
            pages=pages,
            page=page,
            limit=limit,
            prev=prev,
            next=next,
        )
