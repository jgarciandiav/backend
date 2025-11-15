from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import FacturaCreate, FacturaOut
from crud import factura_crud
from auth.auth_bearer import get_current_user

router = APIRouter()

@router.post("/", response_model=FacturaOut)
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    return factura_crud.create_factura(db, factura)

@router.get("/", response_model=list[FacturaOut])
def list_facturas(cobrado: bool = None, customer: str = None, db: Session = Depends(get_db)):
    return factura_crud.list_facturas(db, cobrado, customer)

@router.get("/{nofactura}", response_model=FacturaOut)
def get_factura(nofactura: str, db: Session = Depends(get_db)):
    return factura_crud.get_factura(db, nofactura)

@router.put("/{nofactura}", response_model=FacturaOut)
def update_factura(nofactura: str, factura: FacturaCreate, db: Session = Depends(get_db)):
    return factura_crud.update_factura(db, nofactura, factura)

@router.delete("/{nofactura}")
def delete_factura(nofactura: str, db: Session = Depends(get_db)):
    return factura_crud.delete_factura(db, nofactura)

@router.get("/resumen_facturas")
def resumen(db: Session = Depends(get_db)):
    return factura_crud.resumen(db)

@router.get("/servicios/usados")
def servicios_usados(db: Session = Depends(get_db)):
    return factura_crud.servicios_usados(db)