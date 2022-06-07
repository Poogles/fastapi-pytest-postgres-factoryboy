from typing import cast
from uuid import UUID

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID as PUUID

PostgreSQLUUID = cast(
    "sqlalchemy.types.TypeEngine[UUID]",
    PUUID(as_uuid=True),
)
