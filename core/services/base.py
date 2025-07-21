import asyncio

from sqlalchemy import desc, asc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ColumnSet
from sqlalchemy.sql.functions import count

from core.common.constants import SortType
from core.common.database import AsyncScopedSession
from core.schemas.base import MSBaseSchema


class MSBaseService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def pagination(
        self,
        query_builder: select,
        page=1,
        limit=100,
        sort_by=None,
        sort_type=SortType.ASC,
        is_fetch_all=False,
        schema_class=None,
        no_pagination=False,
    ):
        try:
            if no_pagination:
                page, limit = None, None

            async with asyncio.TaskGroup() as tg:
                count_task = tg.create_task(self._count_queryset(query_builder))
                fetch_records = tg.create_task(
                    self._fetch_queryset_records(
                        query_builder,
                        page=page,
                        limit=limit,
                        sort_by=sort_by,
                        sort_type=sort_type,
                        is_fetch_all=is_fetch_all,
                        schema_class=schema_class,
                    )
                )
        except ExceptionGroup as e:
            if fetch_records.exception():
                raise fetch_records.exception()

            raise e

        return {
            "total": count_task.result(),
            "items": fetch_records.result(),
            "page": page or 1,
            "limit": limit or count_task.result(),
        }

    async def _count_queryset(self, query_builder: select):
        async with AsyncScopedSession() as session:
            total_rows = (
                await session.execute(select(count(1)).select_from(query_builder))
            ).scalar()
            await session.close()
            return total_rows

    async def _fetch_queryset_records(
        self,
        query_builder: select,
        page=1,
        limit=100,
        sort_by=None,
        sort_type=SortType.ASC,
        is_fetch_all=False,
        schema_class=None,
    ):

        offset = (page - 1) * limit if page and limit else 0
        sort_default = (
            query_builder.froms[0].primary_key[0]
            if isinstance(query_builder.froms[0].primary_key, ColumnSet)
            else query_builder.froms[0].primary_key.columns
        )
        order_stmt = desc(sort_default)
        if sort_by and sort_type != SortType.NONE:
            if sort_type == 1:
                order_stmt = desc(sort_by)
            else:
                order_stmt = asc(sort_by)
        query_builder = query_builder.order_by(order_stmt).limit(limit).offset(offset)

        async with AsyncScopedSession() as session:
            if is_fetch_all:
                records = (await session.execute(query_builder)).fetchall()
            else:
                records = (await session.execute(query_builder)).scalars().all()

            if schema_class is not None:
                if issubclass(schema_class, MSBaseSchema):
                    return schema_class(records, many=True).data
                else:
                    return [schema_class.from_orm(record) for record in records]
            await session.close()
            return records
