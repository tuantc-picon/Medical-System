from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, DateTime, func, select, and_, String, desc, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from core.common.constants import StatusInvoiceEnum, SortType
from math import ceil
from app.common.list_schemas import ListBaseSchema
from core.utils.url import update_page_in_url

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
        request,
        schema_response,
        sort_pagination_data,
    ):
        try:
            limit = sort_pagination_data.limit
            page = sort_pagination_data.page
            no_pagination = sort_pagination_data.no_pagination
            sort_by = sort_pagination_data.sort_by
            sort_type = sort_pagination_data.sort_type

            if not no_pagination:
                stmt = stmt.offset((page - 1) * limit).limit(limit)
            stmt = await BaseService.sort_pagination(stmt, sort_by, sort_type)

            item = await self.db.execute(stmt)
            rows = item.fetchall()

            total = rows[0].total if rows and hasattr(rows[0], "total") else 0
            result = [schema_response.model_validate(row[0]) for row in rows]

            pages = ceil(total / limit) if total > 0 else 1

            url = str(request.url) if not no_pagination and page <= pages else None
            prev = None
            next = None
            if url:
                if page > 1:
                    prev = update_page_in_url(url, page - 1)
                if page < pages:
                    next = update_page_in_url(url, page + 1)
            return ListBaseSchema(
                result=result,
                total=total,
                pages=pages,
                page=page,
                limit=limit,
                prev=prev,
                next=next,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def sort_pagination(
        stmt, sort_by: str = None, sort_type: SortType = SortType.DESC
    ):
        table = stmt.froms[0]
        pk_col = list(table.primary_key)[0]
        order_stmt = desc(pk_col)

        if sort_by and sort_type != SortType.NONE:
            col = table.c.get(sort_by)
            if col is None:
                raise ValueError(f"Column '{sort_by}' not found in table {table.name}")

            col_expr = (
                func.lower(col)
                if hasattr(col.type, "python_type") and col.type.python_type == str
                else col
            )
            order_stmt = desc(col_expr) if sort_type == SortType.DESC else asc(col_expr)

        return stmt.order_by(order_stmt)
