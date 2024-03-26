"""Chat model file."""
from typing import TYPE_CHECKING

import sqlalchemy.orm as orm
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .user import User


class FloodApplication(Base):
    """Flood application model."""

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    quiz: Mapped[list[str]] = mapped_column(
        sa.Text, unique=False, nullable=False
    )
    """ User status """

    form: Mapped[list[str]] = mapped_column(
        sa.Text, unique=False, nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped['User'] = orm.relationship(back_populates='flood_applications', lazy='selectin'
    )