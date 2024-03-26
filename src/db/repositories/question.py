"""Question repository file."""
from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Question
from .abstract import Repository


from ..models.user import User as _User

class QuestionRepo(Repository[Question]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=Question, session=session)

    async def new(
        self,
        user: _User,
        question_text: str,
        answer_text: str | None = None,
    ) -> None:
        """Insert a new user into the database.

        :param user_id: Telegram user id
        :param user_name: Telegram username
        :param first_name: Telegram profile first name
        :param second_name: Telegram profile second name
        :param language_code: Telegram profile language code
        :param is_premium: Telegram user premium status
        :param role: User's role
        :param user_chat: Telegram chat with user.
        """
        await self.session.merge(
            Question(
                question_text=question_text,
                user=user,
                answer_text=answer_text,
            )

        )

    # async def update_answer(self, id: int, answer_text: str) -> None:
    #     """Get user role by id."""
    #     statement = (
    #         update(self.type_model)
    #         .where(self.type_model.__table__.c.id == id)
    #         .values({Question.answer_text: answer_text})
    #     )
    #     await self.session.execute(statement)

