"""Question model file."""
from typing import TYPE_CHECKING

import sqlalchemy.orm as orm
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .user import User

class Question(Base):
    """Flood application model."""

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )

    question_text: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=False
    )

    answer_text: Mapped[str] = mapped_column(
        sa.Text, unique=False, nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped['User'] = orm.relationship(back_populates='questions', lazy='selectin'
    )