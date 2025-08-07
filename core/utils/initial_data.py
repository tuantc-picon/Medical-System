from sqlalchemy import text
from core.common.constants import DefaultRole, count_default_roles
from core.common.database import get_async_db_session
from sqlalchemy.exc import SQLAlchemyError

async def init_roles():
    try:
        async for session in get_async_db_session():
            result = await session.execute(text("SELECT COUNT(*) FROM role"))
            count = result.scalar_one()
            if count == count_default_roles():
                return
            else:
                await session.execute(text("TRUNCATE TABLE role RESTART IDENTITY CASCADE"))
                for role in DefaultRole:
                    await session.execute(
                        text("INSERT INTO role (id, name) VALUES (:id, :name)"),
                        {"id": role.role_id, "name": role.role_name}
                    )

                await session.commit()

    except SQLAlchemyError as e:
        print(f"Error initializing role: {e}")
