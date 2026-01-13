from sqlalchemy.orm import Session
from models import ConfigEmpresa
from schemas import ConfigEmpresaCreate

def create_config_empresa(db: Session, config: ConfigEmpresaCreate):
    db_config = ConfigEmpresa(
        nombre_empresa=config.nombre_empresa,
        cif=config.cif,
        telefono=config.telefono,
        email=config.email,
        cp=config.cp
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

def get_config_empresa(db: Session, id: int):
    return db.query(ConfigEmpresa).filter(ConfigEmpresa.id == id).first()

def list_config_empresas(db: Session):
    return db.query(ConfigEmpresa).all()

def update_config_empresa(db: Session, id: int, config: ConfigEmpresaCreate):
    db.query(ConfigEmpresa).filter(ConfigEmpresa.id == id).update({
        "nombre_empresa": config.nombre_empresa,
        "cif": config.cif,
        "telefono": config.telefono,
        "email": config.email,
        "cp": config.cp
    })
    db.commit()
    return get_config_empresa(db, id)

def delete_config_empresa(db: Session, id: int):
    db.query(ConfigEmpresa).filter(ConfigEmpresa.id == id).delete()
    db.commit()
    return {"ok": True}
