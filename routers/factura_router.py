from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Factura
from schemas import FacturaCreate, FacturaOut
from crud import factura_crud
from auth.auth_bearer import get_current_user
from models import FacturaItems

router = APIRouter()



@router.get("/resumen")
def resumen_general(db: Session = Depends(get_db)):
    try:
        total = db.query(Factura).count()
        cobradas = db.query(Factura).filter(Factura.cobrado == True).count()
        sin_cobrar = db.query(Factura).filter(Factura.cobrado == False).count()

        resultado = {
            "total": total,
            "cobradas": cobradas,
            "sin_cobrar": sin_cobrar
        }

        print("🔎 Resultado:", resultado)  
        return resultado

    except Exception as e:
        print("❌ Error en resumen:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
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
def update_factura(
    nofactura: str,
    payload: FacturaCreate,
    db: Session = Depends(get_db)
):
    try:
        # 1. Actualiza cabecera
        db.query(Factura).filter(Factura.nofactura == nofactura).update(
            {
                "fecha": payload.fecha,
                "customer": payload.customer,
                "address": payload.address,
                "cobrado": payload.cobrado,
                "total": sum(item.importe for item in payload.items),
            }
        )

        # 2. Borra items antiguos
        db.query(FacturaItems).filter(FacturaItems.nofactura == nofactura).delete()

        # 3. Inserta items nuevos
        for item in payload.items:
            db_item = FacturaItems(
                nofactura=payload.nofactura,
                service=item.service,
                importe=item.importe
            )
            db.add(db_item)

        db.commit()
        return db.query(Factura).filter(Factura.nofactura == nofactura).first()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{nofactura}")
def delete_factura(nofactura: str, db: Session = Depends(get_db)):
    return factura_crud.delete_factura(db, nofactura)

@router.get("/resumen_facturas")
def resumen(db: Session = Depends(get_db)):
    return factura_crud.resumen(db)

@router.get("/servicios/usados")
def servicios_usados(db: Session = Depends(get_db)):
    return factura_crud.servicios_usados(db)
