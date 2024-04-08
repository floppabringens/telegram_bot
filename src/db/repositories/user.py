"""User repository file."""
from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role
from ..models import User, Base
from .abstract import Repository

from src.configuration import conf

if TYPE_CHECKING:
    from ..models.question import Question as _Question
class UserRepo(Repository[User]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        user_id: int,
        user_real_name: str | None = None,
        role: Role | None = Role.USER,
        thread_id: int | None = None,
        questions: list[type[Base]] | None = [],
        flood_applications: list[type[Base]] | None = [],
    ) -> None:

        if str(user_id) in conf.admin.admin_id:
            role = Role.ADMINISTRATOR

        await self.session.merge(
            User(
                user_id=user_id,
                user_real_name=user_real_name,
                role=role,
                thread_id=thread_id,
                questions=questions,
                flood_applications=flood_applications

            )

        )


    async def get_role(self, user_id: int) -> Role:
        """Get user role by id."""
        return await self.session.scalar(
            select(User.role).where(User.user_id == user_id).limit(1)
        )

    async def update_role(self, user_id: int, role: Role) -> None:
        """Get user role by id."""
        statement = (
            update(self.type_model)
            .where(self.type_model.__table__.c.user_id == user_id)
            .values({User.role: role})
        )
        await self.session.execute(statement)

    async def update_real_name(self, ident: int | str, name) -> None:

        statement = (
            update(self.type_model)
            .where(self.type_model.__table__.c.user_id == ident)
            .values({User.user_real_name: name})
        )
        await self.session.execute(statement)

    async def update_thread(self, ident: int | str, thread_id) -> None:

        statement = (
            update(self.type_model)
            .where(self.type_model.__table__.c.user_id == ident)
            .values({User.thread_id: thread_id})
        )
        await self.session.execute(statement)




    async def is_thread_exists(self, user_id) -> bool:

        thread_id = await self.session.scalar(
            select(User.thread_id).where(User.user_id == user_id).limit(1)
        )

        if thread_id is not None:
            return True
        else:
            return False

   # async def delete(self, user_id) -> None:
   #      statement = delete(self.type_model).where(User.user_id == user_id)
   #      await self.session.execute(statement)

    async def get_by_thread(self, thread_id: int) -> int:
        user_id = await self.session.scalar(
            select(User.user_id).where(User.thread_id == thread_id).limit(1))
        return user_id