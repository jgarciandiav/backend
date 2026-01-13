from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ConfigEmpresaCreate, ConfigEmpresaOut
from crud import configempresa_crud

router = APIRouter()

@router.post("/", response_model=ConfigEmpresaOut)
def create_config_empresa(config: ConfigEmpresaCreate, db: Session = Depends(get_db)):
    return configempresa_crud.create_config_empresa(db, config)

@router.get("/", response_model=list[ConfigEmpresaOut])
def list_config_empresas(db: Session = Depends(get_db)):
    return configempresa_crud.list_config_empresas(db)

@router.get("/{id}", response_model=ConfigEmpresaOut)
def get_config_empresa(id: int, db: Session = Depends(get_db)):
    config = configempresa_crud.get_config_empresa(db, id)
    if not config:
        raise HTTPException(status_code=404, detail="Configuración de empresa no encontrada")
    return config

@router.put("/{id}", response_model=ConfigEmpresaOut)
def update_config_empresa(id: int, config: ConfigEmpresaCreate, db: Session = Depends(get_db)):
    existing = configempresa_crud.get_config_empresa(db, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Configuración de empresa no encontrada")
    return configempresa_crud.update_config_empresa(db, id, config)

@router.delete("/{id}")
def delete_config_empresa(id: int, db: Session = Depends(get_db)):
    existing = configempresa_crud.get_config_empresa(db, id)
    if not existing:
        raise HTTPException(status_code=404, detail="Configuración de empresa no encontrada")
    return configempresa_crud.delete_config_empresa(db, id)
