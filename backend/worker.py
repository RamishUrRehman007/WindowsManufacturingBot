import asyncio
import logging
from contextlib import asynccontextmanager

import config
from arq import Retry, create_pool
from arq.connections import RedisSettings
from domains import message_domain
from session import AsyncSessionLocal

logger = logging.getLogger(__name__)


@asynccontextmanager
async def get_db() -> AsyncSessionLocal:
    db = AsyncSessionLocal()
    try:
        yield db
        await db.commit()
    except:
        await db.rollback()
        raise
    finally:
        await db.close()


async def process_message_to_llm(ctx, message_id, chat_id):
    try:
        async with get_db() as db_session:
            await message_domain.process_message_to_llm(
                db_session, message_id, chat_id
            )
    except (Exception, asyncio.CancelledError) as e:
        logger.exception("Failed to Process Message to OpenAI")
        # raise Retry(defer=ctx["job_try"] * 1)


async def startup(*args, **kwargs) -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s",
        level=config.LOG_LEVEL,
    )


# WorkerSettings defines the settings to use when creating the work,
# it's used by the arq cli.
# For a list of available settings, see https://arq-docs.helpmanual.io/#arq.worker.Worker
class WorkerSettings:
    functions = [process_message_to_llm]
    redis_settings = config.REDIS_SETTINGS
    job_timeout = 86400
    on_startup = startup


if __name__ == "__main__":
    asyncio.run(main())
