import logging
from contextlib import contextmanager
from typing import Callable, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker

BaseModel = declarative_base()

logger = logging.getLogger(__name__)


class DatabaseException(RuntimeError):
    """
    Exception that happened during work with database session
    """


class Database:
    def __init__(self, uri: str) -> None:
        self._engine = create_engine(uri, connect_args={"check_same_thread": False})

        self.session_factory: Callable[[], Session] = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        )

    def init_database(self) -> None:
        BaseModel.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session: Session = self.session_factory()

        try:
            yield session
        except Exception as e:
            session.rollback()

            raise DatabaseException(
                f"Session rollback because of exception: {e!r}"
            ) from e
        finally:
            session.close()
