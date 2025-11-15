from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ServicioCreate, ServicioOut
from crud import servicio_crud

router = APIRouter()

@router.post("/", response_model=ServicioOut)
def create_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    db_serv = servicio_crud.get_by_name(db, servicio.service)
    if db_serv:
        raise HTTPException(status_code=400, detail="Servicio ya existe")
    return servicio_crud.create(db, servicio)

@router.get("/", response_model=list[ServicioOut])
def list_servicios(db: Session = Depends(get_db)):
    return servicio_crud.list_all(db)

@router.get("/{servicio_id}", response_model=ServicioOut)
def get_servicio(servicio_id: int, db: Session = Depends(get_db)):
    srv = servicio_crud.get_by_id(db, servicio_id)
    if not srv:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return srv

@router.put("/{servicio_id}", response_model=ServicioOut)
def update_servicio(servicio_id: int, payload: ServicioCreate, db: Session = Depends(get_db)):
    return servicio_crud.update(db, servicio_id, payload)

@router.delete("/{servicio_id}")
def delete_servicio(servicio_id: int, db: Session = Depends(get_db)):
    servicio_crud.delete(db, servicio_id)
    return {"ok": True}