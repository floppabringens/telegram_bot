# """User repository file."""
#
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.bot.structures.role import Role
#
# from ..models import Base, User
# from .abstract import Repository
#
#
# class UserRepo(Repository[User]):
#     """User repository for CRUD and other SQL queries."""
#
#     def __init__(self, session: AsyncSession):
#         """Initialize user repository as for all users or only for one user."""
#         super().__init__(type_model=User, session=session)
#
#     async def new(
#         self,
#         user_id: int,
#         # chat_id: int,
#         # user_real_name: str | None = None,
#         # flood_application: type[Base] = None,
#         # other: type[Base] = None,
#         # question: type[Base] = None,
#     ) -> None:
#         """Insert a new user into the database.
#
#         :param user_id: Telegram user id
#         :param user_name: Telegram username
#         :param first_name: Telegram profile first name
#         :param second_name: Telegram profile second name
#         :param language_code: Telegram profile language code
#         :param is_premium: Telegram user premium status
#         :param role: User's role
#         :param user_chat: Telegram chat with user.
#         """
#         await self.session.merge(
#             User(
#                 user_id=user_id,
#                 # chat_id=chat_id,
#                 # user_real_name=user_real_name,
#                 # flood_application=flood_application,
#                 # other=other,
#                 # question=question,
#             )
#         )
#
#     # async def get_role(self, user_id: int) -> Role:
#     #     """Get user role by id."""
#     #     return await self.session.scalar(
#     #         select(User.role).where(User.user_id == user_id).limit(1)
#     #     )
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
        questions: list[type[Base]] = []
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
        if str(user_id) in conf.admin_list.admin_id:
            role = Role.ADMINISTRATOR

        await self.session.merge(
            User(
                user_id=user_id,
                user_real_name=user_real_name,
                role=role,
                questions=questions

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


