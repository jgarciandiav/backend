from sqlalchemy.orm import Session
from models import Cliente
from schemas import ClienteCreate

def get_by_name(db: Session, name: str):
    return db.query(Cliente).filter(Cliente.name == name).first()

def get_by_id(db: Session, id: int):
    return db.query(Cliente).filter(Cliente.id == id).first()

def list_all(db: Session):
    return db.query(Cliente).all()

def create(db: Session, obj: ClienteCreate):
    db_obj = Cliente(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, id: int, obj: ClienteCreate):
    db.query(Cliente).filter(Cliente.id == id).update(obj.dict())
    db.commit()
    return get_by_id(db, id)

def delete(db: Session, id: int):
    db.query(Cliente).filter(Cliente.id == id).delete()
    db.commit()