from sqlalchemy.orm import Session
from models import Cliente, Factura
from schemas import ClienteCreate

from sqlalchemy import func

def get_by_name(db: Session, name: str):
    print("🔍 Buscando cliente con nombre:", repr(name.lower()))
    result = db.query(Cliente).filter(func.lower(Cliente.name) == func.lower(name)).first()
    print("✅ Resultado:", result)
    return result

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
    # Get the old customer data before updating
    old_cliente = get_by_id(db, id)
    if not old_cliente:
        return None
    
    old_name = old_cliente.name
    old_address = old_cliente.address
    
    # Update the customer
    db.query(Cliente).filter(Cliente.id == id).update(obj.dict())
    db.commit()
    
    # Update all invoices (facturas) that have this customer
    # Update customer name if it changed
    if old_name != obj.name:
        db.query(Factura).filter(Factura.customer == old_name).update({
            "customer": obj.name
        })
    
    # Update address for all invoices with this customer (using new name)
    # This handles both cases: name changed or address changed
    db.query(Factura).filter(Factura.customer == obj.name).update({
        "address": obj.address
    })
    
    db.commit()
    return get_by_id(db, id)

def delete(db: Session, id: int):
    db.query(Cliente).filter(Cliente.id == id).delete()
    db.commit()

