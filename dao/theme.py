from typing import Any, Dict, Optional, Union, List
from uuid import UUID
from sqlalchemy.orm import Session

from dao.base import BaseDAO
from models.theme import Theme, RecognitionTheme, ApprovedTheme
from schemas.theme import (Theme as ThemeSchema,
                           RecognitionThemeCreate,
                           ApprovedTheme as ApprovedhemeSchema,
                           ApprovedThemeCreate)

from datetime import datetime

class ThemeDAO(BaseDAO[Theme, ThemeSchema, ThemeSchema]):
    
    def get_by_name(self,  db: Session, *, name: str) -> Optional[Theme]:
        return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, *, obj_in: ThemeSchema) -> Theme:
        theme = self.get_by_name(db, name = obj_in.name)
        if theme:
            return theme
        theme = Theme(
            name=obj_in.name,
        )
        db.add(theme)
        db.commit()
        db.refresh(theme)
        return theme


_dao_theme = ThemeDAO(Theme)


class RecognitionThemeDAO(BaseDAO[RecognitionTheme, RecognitionThemeCreate, RecognitionThemeCreate]):
    
    # def get_by_message_id(self,  db: Session, *, name: str) -> List[Optional[RecognitionTheme]]:
    #     return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, *, obj_in: RecognitionThemeCreate) -> RecognitionTheme:
        theme_schematized = ThemeSchema(name = obj_in.name)
        theme = _dao_theme.create(db, obj_in = theme_schematized)

        theme = RecognitionTheme(
            theme=theme,
            message_id=obj_in.message_id,
            probability = obj_in.probability
        )
        db.add(theme)
        db.commit()
        db.refresh(theme)
        return theme


dao_theme = RecognitionThemeDAO(RecognitionTheme) 


class ApprovedThemeDAO(BaseDAO[ApprovedTheme, ApprovedThemeCreate, ApprovedThemeCreate]):
    
    # def get_by_message_id(self,  db: Session, *, name: str) -> List[Optional[RecognitionBlock]]:
    #     return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, *, obj_in: ApprovedThemeCreate) :
        theme_schematized = ThemeSchema(name = obj_in.name)
        theme = _dao_theme.create(db, obj_in = theme_schematized)

        a_theme = ApprovedTheme(
            theme=theme,
        )
        db.add(a_theme)
        db.commit()
        db.refresh(a_theme)
        from dao.message import dao_message
        print(a_theme)
        print(a_theme.id)
        msg = dao_message.set_approved_theme(db, message_id=obj_in.message_id, approved_theme_id=a_theme.id)
        return msg

dao_approvedtheme = ApprovedThemeDAO(ApprovedTheme) 