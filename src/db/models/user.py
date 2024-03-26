"""User model file."""
from typing import TYPE_CHECKING

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.bot.structures.role import Role

from .base import Base


if TYPE_CHECKING:
    from .question import Question
    from .flood_application import FloodApplication


class User(Base):
    """User model."""

    user_id: Mapped[int] = mapped_column(
        sa.BigInteger, unique=True, nullable=False, primary_key=True
    )
    """ Telegram user id """

    user_real_name: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )

    role: Mapped[Role] = mapped_column(sa.Enum(Role), default=Role.USER)
    """ User's role """

    questions: Mapped[list['Question']] = orm.relationship(back_populates='user', lazy='selectin'
    )

    flood_applications: Mapped[list['FloodApplication']] = orm.relationship(back_populates='user', lazy='selectin'
    )


    #     """ Telegram chat with user """
    #
    #     other_fk: Mapped[int] = mapped_column(
    #         sa.ForeignKey('other.id'), unique=False, nullable=False
    #     )
    #
    #     other: Mapped[FloodApplication] = orm.relationship(
    #         'other', uselist=False, lazy='joined'
    #     )
