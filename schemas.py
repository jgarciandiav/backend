from pydantic import BaseModel, ConfigDict, field_validator, field_serializer
from typing import List, Optional
from datetime import date, datetime

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    is_active: bool = True

class UserLogin(BaseModel):
    username: str
    password: str    

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class ServicioCreate(BaseModel):
    service: str

class ServicioOut(BaseModel):
    id: int
    service: str
    model_config = ConfigDict(from_attributes=True)

class ClienteCreate(BaseModel):
    name: str
    address: str

class ClienteOut(BaseModel):
    id: int
    name: str
    address: str
    model_config = ConfigDict(from_attributes=True)

class FacturaItemCreate(BaseModel):
    service: str
    importe: float

class FacturaCreate(BaseModel):
    nofactura: str
    fecha: date
    customer: str
    address: str
    items: List[FacturaItemCreate]
    cobrado: bool = False

    @field_validator('fecha', mode='before')
    @classmethod
    def parse_fecha_eu(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()
            except ValueError:
                try:
                    return datetime.strptime(v, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError('Formato de fecha inválido. Usa DD/MM/YYYY o YYYY-MM-DD')
        return v

class FacturaOut(BaseModel):
    id: int
    nofactura: str
    fecha: date
    customer: str
    address: str
    total: float
    cobrado: bool
    model_config = ConfigDict(from_attributes=True)

    @field_serializer('fecha')
    def serialize_fecha(self, value: date, _info):
        return value.strftime('%d/%m/%Y')

class FacturaItemOut(BaseModel):
    id: int
    nofactura: str
    service: str
    importe: float
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLoginResponse(BaseModel):
    access_token: str        # opcional, bórralo si NO quieres token
    token_type: str
    full_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class ConfigEmpresaCreate(BaseModel):
    nombre_empresa: str
    cif: str
    telefono: str
    email: str
    cp: str

class ConfigEmpresaOut(BaseModel):
    id: int
    nombre_empresa: str
    cif: str
    telefono: str
    email: str
    cp: str
    model_config = ConfigDict(from_attributes=True)

class ResumenClienteOut(BaseModel):
    customer: str
    suma_pagadas: float
    suma_pendientes: float
    total: float
    cantidad_facturas: int
    model_config = ConfigDict(from_attributes=True)

class FechaQuery(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    @field_validator('fecha_inicio', 'fecha_fin', mode='before')
    @classmethod
    def parse_fecha_eu(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d/%m/%Y').date()
            except ValueError:
                try:
                    return datetime.strptime(v, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError('Formato de fecha inválido. Usa DD/MM/YYYY o YYYY-MM-DD')
        return v