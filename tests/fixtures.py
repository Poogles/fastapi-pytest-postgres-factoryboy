import random
import string
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from time import time
from typing import Any, Callable, Dict, Generator, List, Optional, Union
from uuid import uuid4

import factory
import faker
import pytest

from app.dependencies import get_db
from app.models import Company

fake = faker.Factory.create()


@pytest.fixture(scope="function")
def company_factory_function(client_function) -> Any:
    class CompanyFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore  # noqa
        id = factory.LazyAttribute(lambda _: fake.uuid4())
        name = factory.Sequence(
            lambda n: f"{fake.company()} {n} "
            + "".join(random.choice(string.ascii_uppercase) for _ in range(3))
        )

        class Meta:
            model = Company
            sqlalchemy_session = next(
                client_function.app.dependency_overrides[get_db]()
            )
            sqlalchemy_session_persistence = "commit"

    yield CompanyFactory


@pytest.fixture(scope="session")
def company_factory_session(client_session) -> Any:
    class CompanyFactory(factory.alchemy.SQLAlchemyModelFactory):  # type: ignore  # noqa
        id = factory.LazyAttribute(lambda _: fake.uuid4())
        name = factory.Sequence(
            lambda n: f"{fake.company()} {n} "
            + "".join(random.choice(string.ascii_uppercase) for _ in range(3))
        )

        class Meta:
            model = Company
            sqlalchemy_session = next(client_session.app.dependency_overrides[get_db]())
            sqlalchemy_session_persistence = "commit"

    yield CompanyFactory
