from contextlib import contextmanager
import logging

import pytest
import pytest_postgresql.factories as pg_factories
from fastapi.testclient import TestClient
from pydantic import PostgresDsn
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.app import app
from app.db import Base
from app.dependencies import get_db


log = logging.getLogger(__name__)


postgresql = pg_factories.postgresql_proc()


def build_postgres_dsn(
    host: str, port: int, user: str, password: str, dbname: str
) -> PostgresDsn:
    """Build a postgres DSN from component parts."""
    return PostgresDsn.build(
        scheme="postgresql",
        host=host,
        port=str(port),
        user=user,
        password=password,
        path="/" + dbname + "_tmpl",
    )


@contextmanager
def nested_transaction_manager(engine, sessionmaker):

    # connect to the database
    connection = engine.connect()

    # begin a non-ORM transaction
    trans = connection.begin()

    # bind an individual Session to the connection
    session = sessionmaker(bind=connection)
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()

    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    trans.rollback()

    # return connection to the Engine
    connection.close()


@pytest.fixture(scope="session")
def db(postgresql):
    engine = create_engine(
        build_postgres_dsn(
            "127.0.0.1",
            postgresql.port,
            postgresql.user,
            postgresql.password,
            postgresql.dbname,
        ),
    )
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine, TestSession


@pytest.fixture(scope="session")
def _client(db):
    engine, TestSession = db

    # Spawn the database.
    Base.metadata.create_all(bind=engine)

    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def client_session(_client, db):
    engine, TestSession = db

    def override_get_db():
        try:
            db = TestSession()
            yield db
        finally:
            db.close()

    _client.app.dependency_overrides[get_db] = override_get_db

    yield _client


@pytest.fixture(scope="function")
def client_function(_client, db):
    engine, TestSession = db
    with nested_transaction_manager(engine, TestSession) as TransactionalTestSession:

        # Create new override that rolls back.
        def override_get_db_rollbacks():
            yield TransactionalTestSession

        _client.app.dependency_overrides[get_db] = override_get_db_rollbacks

        yield _client


# Import our other fixtures.
pytest_plugins = [
    "tests.fixtures",
]
