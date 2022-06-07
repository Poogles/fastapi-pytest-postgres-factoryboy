from typing import NewType, cast
from uuid import UUID, uuid4

from sqlalchemy import Column, String, types

from app.common import PostgreSQLUUID
from app.db import Base

CompanyId = NewType("CompanyId", UUID)
_CompanyId = cast("types.TypeEngine[CompanyId]", PostgreSQLUUID)


class Company(Base):
    __tablename__ = "companies"

    id = Column(_CompanyId, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
