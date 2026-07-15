from sqlalchemy.orm import Session
from typing import Any, TypeVar, Generic, Type

ModelType = TypeVar("ModelType")
SchemaCreateType = TypeVar("SchemaCreateType")
SchemaUpdateType = TypeVar("SchemaUpdateType")

class CRUDBase(Generic[ModelType, SchemaCreateType, SchemaUpdateType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: dict | SchemaCreateType):
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            db_obj = self.model(**obj_in.model_dump())
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, id: int, obj_in: SchemaUpdateType) -> Any:
        db_obj = self.get(db, id)
        if not db_obj:
            return None
        
        update_data = obj_in.dict(exclude_unset=True) 
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    