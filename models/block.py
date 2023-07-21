from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from db.base_class import Base

    
class Block(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String, unique=True)


class RecognitionBlock(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    probability = Column(Float)

    block_id = Column(UUID(as_uuid=True), ForeignKey('block.id'))
    block = relationship('Block')

    message_id = Column(UUID(as_uuid=True), ForeignKey('message.id'))
    message = relationship('Message', back_populates="recognition_blocks")

    @hybrid_property
    def name(self):
        return self.block.name


class ApprovedBlock(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    
    block_id = Column(UUID(as_uuid=True), ForeignKey('block.id'))
    block = relationship('Block')
    
    message = relationship('Message', back_populates='block')
    

