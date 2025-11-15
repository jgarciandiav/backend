from sqlalchemy.orm import Session
from models import Servicio
from schemas import ServicioCreate

def get_by_name(db: Session, name: str):
    return db.query(Servicio).filter(Servicio.service == name).first()

def get_by_id(db: Session, id: int):
    return db.query(Servicio).filter(Servicio.id == id).first()

def list_all(db: Session):
    return db.query(Servicio).all()

def create(db: Session, obj: ServicioCreate):
    db_obj = Servicio(**obj.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, id: int, obj: ServicioCreate):
    db.query(Servicio).filter(Servicio.id == id).update(obj.dict())
    db.commit()
    return get_by_id(db, id)

def delete(db: Session, id: int):
    db.query(Servicio).filter(Servicio.id == id).delete()
    db.commit()