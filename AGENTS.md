# Agent Guidelines for FastAPI Invoicing System

## Project Overview
This is a FastAPI backend for an invoicing system (Sistema de Facturación) with SQLite database, JWT authentication, and SQLAlchemy ORM. The API provides user management, service catalog, client management, and invoice generation functionality.

## Build/Lint/Test Commands

### Running the Application
```bash
uvicorn main:app --reload
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Testing
No tests are currently configured. When adding tests, use pytest and create test files named `test_*.py`.

## Code Style Guidelines

### Import Organization
Order imports from top to bottom:
1. Standard library imports
2. Third-party imports (fastapi, sqlalchemy, pydantic, etc.)
3. Local imports (from database, from models, from schemas, from crud, from auth)

Example:
```python
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Factura
from schemas import FacturaCreate, FacturaOut
```

### Naming Conventions
- **Models**: PascalCase (User, Factura, FacturaItems)
- **Database tables**: snake_case in `__tablename__` (users, facturas, facturaitems)
- **Columns**: snake_case (full_name, nofactura, cobrado)
- **Functions**: snake_case (get_db, create_factura)
- **Variables**: snake_case (db_factura, access_token)
- **Constants**: UPPER_SNAKE_CASE (SECRET_KEY, ALGORITHM)
- **Router instances**: `router`
- **CRUD modules**: `{entity}_crud.py` (factura_crud.py, user_crud.py)

### File Structure
- `main.py` - Application entry point, FastAPI app, CORS setup, router registration
- `database.py` - SQLAlchemy engine, session factory, Base declarative base, get_db dependency
- `models.py` - SQLAlchemy ORM models (table definitions)
- `schemas.py` - Pydantic schemas for request/response validation
- `routers/` - API route handlers grouped by domain
- `crud/` - Database operations (create, read, update, delete, custom queries)
- `auth/` - Authentication (JWT token creation, password hashing) and authorization

### Pydantic Schemas
- Use PascalCase classes inheriting from BaseModel
- Separate Create/Out schemas for input/output validation
- Use appropriate types (str, int, float, bool, date, List)
- For output schemas, always include: `model_config = ConfigDict(from_attributes=True)`

Example:
```python
class FacturaCreate(BaseModel):
    nofactura: str
    fecha: date
    customer: str
    items: List[FacturaItemCreate]
    cobrado: bool = False

class FacturaOut(BaseModel):
    id: int
    nofactura: str
    fecha: date
    total: float
    cobrado: bool
    model_config = ConfigDict(from_attributes=True)
```

### Database Operations
- Always use `db: Session = Depends(get_db)` dependency injection in route handlers
- Use `db.commit()` after add/update operations, then `db.refresh()` to get updated values
- Use `db.rollback()` in except blocks when performing multiple operations
- Use `db.query(Model).filter(...).first()` for single results
- Use `db.query(Model).filter(...).all()` for multiple results
- Use `.count()` for counting queries

Example transaction handling:
```python
try:
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura
except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=str(e))
```

### Route Handler Patterns
- Use `APIRouter()` for route modules, import in main.py and register with prefix and tags
- HTTP methods: `@router.get("/")`, `@router.post("/")`, `@router.put("/")`, `@router.delete("/")`
- Always include `response_model` parameter for proper output validation
- Use `Query()` for optional query parameters with validation
- Use path parameters like `/{id}` for resource lookup
- Raise `HTTPException` for errors: `raise HTTPException(status_code=404, detail="Not found")`

Example:
```python
@router.get("/{nofactura}", response_model=FacturaOut)
def get_factura(nofactura: str, db: Session = Depends(get_db)):
    return factura_crud.get_factura(db, nofactura)
```

### Error Handling
- Use `HTTPException` with appropriate status codes:
  - 400 for validation errors
  - 401 for authentication errors
  - 404 for not found
  - 500 for server errors
- Always wrap complex operations in try/except with `db.rollback()`
- Return error messages in Spanish to match existing code

### Authentication
- JWT tokens using `python-jose` with HS256 algorithm
- Password hashing with bcrypt via passlib (truncated to 72 bytes)
- Token expiration: 30 minutes
- Use `get_current_user` dependency from `auth.auth_bearer` for protected routes
- Login route returns: access_token, token_type, full_name, email

### CORS Configuration
- Allowed origin: `http://localhost:5173` (Vite dev server)
- All methods and headers allowed
- Credentials enabled

### Database Configuration
- SQLite database file: `facturacion.db` (gitignored)
- Engine created with `check_same_thread=False` for SQLite compatibility
- Auto-creates tables on startup: `Base.metadata.create_all(bind=engine)`
- Use SQLAlchemy declarative base patterns

### Spanish Language
- All user-facing text, comments, and error messages should be in Spanish
- Variable names in English/Spanglish is acceptable (e.g., nofactura, cobrado)

### Important Notes
- Never commit `facturacion.db` to git
- Always use the CRUD layer for database operations, never query directly in routers
- Follow existing patterns when adding new entities (Model, Schema, CRUD, Router)
- The database file is SQLite and gets auto-created on first run
