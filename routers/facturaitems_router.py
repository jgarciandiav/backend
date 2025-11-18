from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
from models import FacturaItems
from schemas import FacturaItemOut

router = APIRouter()

@router.get("/", response_model=list[FacturaItemOut])
def listar_items_por_factura(
    nofactura: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    items = db.query(FacturaItems).filter(FacturaItems.nofactura == nofactura).all()
    if not items:
        raise HTTPException(status_code=404, detail="No hay items para esta factura")
    return items