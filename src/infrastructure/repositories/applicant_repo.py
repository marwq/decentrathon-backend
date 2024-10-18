from datetime import date, datetime, timedelta
from typing import Sequence

from sqlalchemy import select, insert

from src.infrastructure.models.applicant import UserApplicant, Experience, Skill
from src.infrastructure.repositories.base import SQLAlchemyRepo


class ApplicantRepo(SQLAlchemyRepo[UserApplicant]):
    """User Applicant repository implementation for SQLAlchemy ORM."""
    
    model = UserApplicant
    
    async def upsert_user_applicant(
        self,
        user_id: int,
        job_title: str | None,
        job_salary: str | None,
        experiences_data: list[dict],
        skills_data: list[dict]
    ) -> UserApplicant:
        stmt = select(UserApplicant).where(UserApplicant.user_id == user_id)
        result = await self._session.execute(stmt)
        existing_applicant = result.scalar_one_or_none()
        
        if existing_applicant:
            existing_applicant.job_title = job_title
            existing_applicant.job_salary = job_salary
        else:
            existing_applicant = UserApplicant(
                user_id=user_id,
                job_title=job_title,
                job_salary=job_salary
            )
            self._session.add(existing_applicant)
        
        if existing_applicant.experiences:
            for experience in existing_applicant.experiences:
                await self._session.delete(experience)
        
        new_experiences = [
            Experience(
                user_id=user_id,
                title=exp_data['title'],
                start_at=exp_data['start_at'].replace(tzinfo=None) if exp_data['start_at'].tzinfo else exp_data['start_at'],
                end_at=exp_data.get('end_at').replace(tzinfo=None) if exp_data.get('end_at') and exp_data['end_at'].tzinfo else exp_data.get('end_at'),
                description=exp_data['description'],
                company_name=exp_data['company_name']
            )
            for exp_data in experiences_data
        ]
        existing_applicant.experiences = new_experiences
        
        if existing_applicant.skills:
            for skill in existing_applicant.skills:
                await self._session.delete(skill)
        
        new_skills = [
            Skill(
                user_id=user_id,
                title=skill_data['title'],
            )
            for skill_data in skills_data
        ]
        existing_applicant.skills = new_skills
        
        await self._session.commit()
        await self._session.refresh(existing_applicant)
        
        return existing_applicant

    