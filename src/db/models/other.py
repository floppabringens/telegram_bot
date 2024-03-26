# """Chat model file."""
# import sqlalchemy as sa
# from sqlalchemy.orm import Mapped, mapped_column
#
# from .base import Base
#
#
# class Other(Base):
#     """Flood application model."""
#
#     other_text: Mapped[str] = mapped_column(
#         sa.Text, unique=False, nullable=False
#     )
#
#     other_answer_text: Mapped[str] = mapped_column(
#         sa.Text, unique=False, nullable=True
#     )
#
#     user: Mapped[int] = mapped_column(
#         sa.ForeignKey('user.id', ondelete='CASCADE'),
#         unique=False,
#         nullable=True,
#     )
#     """ Foreign key to user (it can has effect only in private chats) """
