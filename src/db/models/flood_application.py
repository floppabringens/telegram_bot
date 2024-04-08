"""Chat model file."""
from typing import TYPE_CHECKING

import sqlalchemy.orm as orm
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from ...bot.structures.status import Status

if TYPE_CHECKING:
    from .user import User


class FloodApplication(Base):
    """Flood application model."""

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    details: Mapped[list[str]] = mapped_column(
        sa.ARRAY(sa.Text), unique=False, nullable=False
    )

    form: Mapped[list[str]] = mapped_column(
        sa.ARRAY(sa.Text), unique=False, nullable=False
    )

    documents: Mapped[list[str]] = mapped_column(
        sa.ARRAY(sa.Text), unique=False, nullable=False
    )

    pdf_id: Mapped[str] = mapped_column(
        unique=True, nullable=True
    )


    status: Mapped[Status] = mapped_column(sa.Enum(Status), default=Status.NEW)


    is_deleted: Mapped[bool] = mapped_column(
        nullable=False, default=False
    )

    moder_message_id: Mapped[int] = mapped_column(
        unique=True, nullable=True
    )

    user_message_id: Mapped[int] = mapped_column(
        unique=True, nullable=True
    )

    price: Mapped[int] = mapped_column(
        unique=False, nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped['User'] = orm.relationship(back_populates='flood_applications', lazy='selectin'
    )