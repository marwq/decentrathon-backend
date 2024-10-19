from src.infrastructure.cache import redis_client
from src.infrastructure.uow import SQLAlchemyUoW
from src.infrastructure.models import UserApplicant, Job


async def get_jobs_count(
    uow: SQLAlchemyUoW
) -> int:
    count = await redis_client.get("jobs_count")
    if count is None:
        count = await uow.job_repo.count()
        await redis_client.set("jobs_count", count, expire=30)
    return count

def get_job_relevance(applicant: UserApplicant, job: Job) -> str | None:
    matches = {skill.title.capitalize() for skill in applicant.skills if skill.title.lower() in job.details.lower()}
    return matches or None