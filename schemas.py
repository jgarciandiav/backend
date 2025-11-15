from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import date

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

class FacturaOut(BaseModel):
    id: int
    nofactura: str
    fecha: date
    customer: str
    address: str
    total: float
    cobrado: bool
    model_config = ConfigDict(from_attributes=True)

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