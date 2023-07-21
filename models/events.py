from typing import TYPE_CHECKING
import enum
from sqlalchemy import ForeignKey, Column, LargeBinary, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base
from uuid import uuid4
# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401


class Events(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)

    document_id = Column(UUID(as_uuid=True), ForeignKey('document.id'))
    document = relationship('Document', back_populates='events')

    file_events = Column(LargeBinary)
    file_messages = Column(LargeBinary)
