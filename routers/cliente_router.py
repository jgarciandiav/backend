from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ClienteCreate, ClienteOut
from crud import cliente_crud

router = APIRouter()

@router.post("/", response_model=ClienteOut)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cli = cliente_crud.get_by_name(db, cliente.name)
    if db_cli:
        raise HTTPException(status_code=400, detail="Cliente ya existe")
    return cliente_crud.create(db, cliente)

@router.get("/", response_model=list[ClienteOut])
def list_clientes(db: Session = Depends(get_db)):
    return cliente_crud.list_all(db)

@router.get("/{cliente_id}", response_model=ClienteOut)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cli = cliente_crud.get_by_id(db, cliente_id)
    if not cli:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cli

@router.put("/{cliente_id}", response_model=ClienteOut)
def update_cliente(cliente_id: int, payload: ClienteCreate, db: Session = Depends(get_db)):
    return cliente_crud.update(db, cliente_id, payload)

@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente_crud.delete(db, cliente_id)
    return {"ok": True}