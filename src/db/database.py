"""Database class with all-in-one features."""

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from src.configuration import conf

from .repositories import QuestionRepo, UserRepo, FloodApplicationRepo


def create_async_engine(url: URL | str) -> AsyncEngine:
    """Create async engine with given URL.

    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=conf.debug, pool_pre_ping=True)


class Database:
    """Database class.

    is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions.
    """

    user: UserRepo
    """ User repository """
    question: QuestionRepo
    """ Chat repository """

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo = None,
        question: QuestionRepo = None,
        flood_application: FloodApplicationRepo = None,
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        :param user: (Optional) User repository
        :param chat: (Optional) Chat repository
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.question = question or QuestionRepo(session=session)
        self.flood_application = flood_application or FloodApplicationRepo(session=session)

