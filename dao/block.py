from typing import Any, Dict, Optional, Union, List
from uuid import UUID
from sqlalchemy.orm import Session

from dao.base import BaseDAO
from dao.message import dao_message
from models.block import Block, RecognitionBlock, ApprovedBlock
from schemas.block import (Block as BlockSchema,
                           RecognitionBlockCreate,
                           ApprovedBlockCreate,
                           ApprovedBlock as ApprovedBlockSchema)

from datetime import datetime

class BlockDAO(BaseDAO[Block, BlockSchema, BlockSchema]):
    
    def get_by_name(self,  db: Session, *, name: str) -> Optional[Block]:
        return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, *, obj_in: BlockSchema) -> Block:
        block = self.get_by_name(db, name = obj_in.name)
        if block:
            return block
        block = Block(
            name=obj_in.name,
        )
        db.add(block)
        db.commit()
        db.refresh(block)
        return block


_dao_block = BlockDAO(Block)


class RecognitionBlockDAO(BaseDAO[RecognitionBlock, RecognitionBlockCreate, RecognitionBlockCreate]):
    
    # def get_by_message_id(self,  db: Session, *, name: str) -> List[Optional[RecognitionBlock]]:
    #     return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, *, obj_in: RecognitionBlockCreate) -> RecognitionBlock:
        block_schematized = BlockSchema(name = obj_in.name)
        block = _dao_block.create(db, obj_in = block_schematized)

        block = RecognitionBlock(
            block=block,
            message_id=obj_in.message_id,
            probability = obj_in.probability
        )
        db.add(block)
        db.commit()
        db.refresh(block)
        return block


dao_block = RecognitionBlockDAO(RecognitionBlock) 


class ApprovedBlockDAO(BaseDAO[ApprovedBlock, ApprovedBlockCreate, ApprovedBlockCreate]):
    
    # def get_by_message_id(self,  db: Session, *, name: str) -> List[Optional[RecognitionBlock]]:
    #     return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, *, obj_in: ApprovedBlockCreate):
        block_schematized = BlockSchema(name = obj_in.name)
        block = _dao_block.create(db, obj_in = block_schematized)

        block = ApprovedBlock(
            block=block,
        )
        db.add(block)
        db.commit()
        db.refresh(block)

        from dao.message import dao_message
        msg = dao_message.set_approved_block(db, message_id=obj_in.message_id, approved_block_id=block.id)
        return msg

dao_approvedblock = ApprovedBlockDAO(ApprovedBlock) 