from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

class Servicio(Base):
    __tablename__ = "servicios"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, unique=True, index=True)

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    nofactura = Column(String, unique=True, index=True)
    fecha = Column(Date)
    customer = Column(String)
    address = Column(String)
    total = Column(Float)
    cobrado = Column(Boolean, default=False)

class FacturaItems(Base):
    __tablename__ = "facturaitems"
    id = Column(Integer, primary_key=True, index=True)
    nofactura = Column(String, ForeignKey("facturas.nofactura"))
    service = Column(String)
    importe = Column(Float)