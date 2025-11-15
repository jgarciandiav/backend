from sqlalchemy.orm import Session
from models import Factura, FacturaItems, Cliente, Servicio
from schemas import FacturaCreate
from sqlalchemy import func

def create_factura(db: Session, factura: FacturaCreate):
    # Validar o crear cliente
    cliente = db.query(Cliente).filter(Cliente.name == factura.customer).first()
    if not cliente:
        cliente = Cliente(name=factura.customer, address=factura.address)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)

    # Crear factura
    total = sum(item.importe for item in factura.items)
    db_factura = Factura(
        nofactura=factura.nofactura,
        fecha=factura.fecha,
        customer=factura.customer,
        address=factura.address,
        total=total,
        cobrado=factura.cobrado
    )
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)

    # Crear items
    for item in factura.items:
        servicio = db.query(Servicio).filter(Servicio.service == item.service).first()
        if not servicio:
            servicio = Servicio(service=item.service)
            db.add(servicio)
            db.commit()
            db.refresh(servicio)

        db_item = FacturaItems(
            nofactura=factura.nofactura,
            service=item.service,
            importe=item.importe
        )
        db.add(db_item)

    db.commit()
    return db_factura

def list_facturas(db: Session, cobrado: bool = None, customer: str = None):
    query = db.query(Factura)
    if cobrado is not None:
        query = query.filter(Factura.cobrado == cobrado)
    if customer:
        query = query.filter(Factura.customer.ilike(f"%{customer}%"))
    return query.all()

def get_factura(db: Session, nofactura: str):
    return db.query(Factura).filter(Factura.nofactura == nofactura).first()

def update_factura(db: Session, nofactura: str, factura: FacturaCreate):
    db_factura = get_factura(db, nofactura)
    if not db_factura:
        return None
    for key, value in factura.dict(exclude={"items"}).items():
        setattr(db_factura, key, value)
    db.commit()
    db.refresh(db_factura)
    return db_factura

def delete_factura(db: Session, nofactura: str):
    db.query(FacturaItems).filter(FacturaItems.nofactura == nofactura).delete()
    db.query(Factura).filter(Factura.nofactura == nofactura).delete()
    db.commit()
    return {"ok": True}

def resumen(db: Session):
    total = db.query(func.count(Factura.id)).scalar()
    cobradas = db.query(func.count(Factura.id)).filter(Factura.cobrado == True).scalar()
    no_cobradas = total - cobradas
    return {"total": total, "cobradas": cobradas, "no_cobradas": no_cobradas}

def servicios_usados(db: Session):
    from sqlalchemy import distinct
    return db.query(distinct(FacturaItems.service)).all()