import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete

from config import (REFRESH_TOKEN_EXPIRED)
from core.common.Base import BaseService
from core.common.database import get_async_db_session
from core.models.schedule import ScheduleDoctor
from core.models.token import ListToken


class clean_table(BaseService):
    @staticmethod
    async def clean_expired_token():
        expired_delta = timedelta(minutes=REFRESH_TOKEN_EXPIRED)
        while True:
            try:
                async for session in get_async_db_session():
                    now = datetime.now(timezone.utc)
                    await session.execute(
                        delete(ListToken).where(
                            ListToken.created_at < now - expired_delta
                        )
                    )
                    await session.commit()
                    break
            except Exception as e:
                print(f"[clean_expired_token] Error: {e}")
            await asyncio.sleep(3600)

    @staticmethod
    async def clean_schedule_doctor_expired():
        while True:
            try:
                async for session in get_async_db_session():
                    now = datetime.now(timezone.utc)
                    await session.execute(
                        delete(ScheduleDoctor).where(
                            ScheduleDoctor.end_time < now
                        )
                    )
                    await session.commit()
                    break
            except Exception as e:
                print(f"[clean_schedule_doctor] Error: {e}")
            await asyncio.sleep(43200)
