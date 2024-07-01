import uuid
from datetime import datetime
from typing import Annotated
from typing import Any
from typing import ClassVar

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column

UuidPK = Annotated[
    uuid.UUID,
    mapped_column(
        Uuid,
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    ),
]

StrUnique = Annotated[str, mapped_column(Text, unique=True)]
Txt = Annotated[str, mapped_column(String, server_default='')]
CurrencyFK = Annotated[
    uuid.UUID,
    mapped_column(ForeignKey('currencies.id', ondelete='CASCADE')),
]
ProductTypeFK = Annotated[
    uuid.UUID,
    mapped_column(ForeignKey('product_types.id', ondelete='CASCADE')),
]
UnitPK = Annotated[
    uuid.UUID,
    mapped_column(ForeignKey('units.id', ondelete='CASCADE')),
]
SupplierFK = Annotated[
    uuid.UUID,
    mapped_column(ForeignKey('suppliers.id', ondelete='CASCADE')),
]
CreatedAt = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    ),
]
UpdatedAt = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
]


class BaseModel(DeclarativeBase):
    """Base class for orm models."""

    type_annotation_map: ClassVar[dict[Any, Any]] = {
        datetime: DateTime(timezone=True),
    }
