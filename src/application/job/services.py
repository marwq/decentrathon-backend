from src.infrastructure.cache import redis_client
from src.infrastructure.uow import SQLAlchemyUoW
from src.infrastructure.models import UserApplicant, Job


async def get_jobs_count(
    uow: SQLAlchemyUoW,
    **kwargs
) -> int:
    count = await redis_client.get(f"jobs_count:{str(kwargs).__hash__()}")
    if count is None:
        count = await uow.job_repo.count_jobs(**kwargs)
        await redis_client.set(f"jobs_count:{str(kwargs).__hash__()}", count, expire=30)
    return count

def get_job_relevance(applicant: UserApplicant, job: Job) -> str | None:
    matches = {skill.title.capitalize() for skill in applicant.skills if skill.title.lower() in job.details.lower()}
    return matches or None


