from typing import TYPE_CHECKING
import enum
from sqlalchemy import Enum, Column, LargeBinary, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base
from uuid import uuid4
# if TYPE_CHECKING:
#     from .item import Item  # noqa: F401




class DocumentStatus(str, enum.Enum):
    loaded = "loaded"
    markingup = "markup_in_progress"
    markup = "markedup"
    approving = "partially_approved"
    approve = "approved"

class Document(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String)
    created_at = Column(DateTime)
    file = Column(LargeBinary)
    status = Column(Enum(DocumentStatus))
    messages = relationship('Message', back_populates='document', cascade="all, delete")

    # email = Column(String, unique=True, index=True, nullable=False)
    # hashed_password = Column(String, nullable=False)
    # is_active = Column(Boolean(), default=True)
    # is_superuser = Column(Boolean(), default=False)
    # items = relationship("Item", back_populates="owner")
