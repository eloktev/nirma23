from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from db.base_class import Base

    

class Theme(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String, unique=True)


class RecognitionTheme(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    probability = Column(Float)

    theme_id = Column(UUID(as_uuid=True), ForeignKey('theme.id'))
    theme = relationship('Theme')

    message_id = Column(UUID(as_uuid=True), ForeignKey('message.id'))
    message = relationship('Message', back_populates="recognition_themes")

    @hybrid_property
    def name(self):
        return self.theme.name

class ApprovedTheme(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    
    theme_id = Column(UUID(as_uuid=True), ForeignKey('theme.id'))
    theme = relationship('Theme')
    
    message = relationship('Message', back_populates='theme')
    

