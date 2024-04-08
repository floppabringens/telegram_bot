"""Question repository file."""
from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import FloodApplication
from .abstract import Repository


from ..models.user import User as _User
from ...bot.structures.status import Status


class FloodApplicationRepo(Repository[FloodApplication]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=FloodApplication, session=session)

    async def new(
        self,
        user: _User,
        details: list[str],
        form: list[str],
        documents: list[str],
        pdf_id: str | None = None,
        status: Status | None = Status.NEW,
        is_deleted: bool | None = False,
        moder_message_id: int | None = None,
        user_message_id: int | None = None,
        price: int | None = None,
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
            FloodApplication(
                user=user,
                details=details,
                form=form,
                documents=documents,
                pdf_id=pdf_id,
                status=status,
                is_deleted=is_deleted,
                moder_message_id=moder_message_id,
                user_message_id=user_message_id,
                price=price,
            )

        )

    async def update_pdf_id(self, id: int, pdf_id: str) -> None:
        statement = (
            update(self.type_model)
            .where(self.type_model.__table__.c.id == id)
            .values({FloodApplication.pdf_id: pdf_id})
        )
        await self.session.execute(statement)

    async def update_status(self, id: int, status: Status) -> None:
        statement = (
            update(self.type_model)
            .where(self.type_model.__table__.c.id == id)
            .values({FloodApplication.status: status})
        )
        await self.session.execute(statement)

    async def update_moder_message_id(self, id: int , moder_message_id: int | str) -> None:
        statement = (
            update(self.type_model)
            .where(self.type_model.__table__.c.id == id)
            .values({FloodApplication.moder_message_id: int(moder_message_id)})
        )
        await self.session.execute(statement)

    async def update_is_deleted(self, id: int, is_deleted: bool) -> None:
        statement = (
            update(self.type_model)
            .where(self.type_model.__table__.c.id == id)
            .values({FloodApplication.is_deleted: is_deleted})
        )
        await self.session.execute(statement)