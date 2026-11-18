from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash
from .config import settings
from .database import Base, engine, get_db
from .models import Product, Movement
from .schemas import LoginInput, TokenOutput, ProductCreate, ProductOutput, MovementCreate, MovementOutput, SummaryOutput
from .security import create_access_token, get_current_user


app = FastAPI(title="MVP Controle de Estoque", version="1.0.0")
origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/auth/login", response_model=TokenOutput)
def login(data: LoginInput):
    hasher = PasswordHash.recommended()
    # Verificação direta para o usuário inicial configurado por ambiente.
    # A senha é comparada usando hash Argon2, sem armazenar credenciais no banco.
    if data.username != settings.admin_username:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")
    # Hash calculado para esta demonstração; em produção, armazenar hash persistente de usuário.
    if not hasher.verify(data.password, hasher.hash(settings.admin_password)):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")
    return TokenOutput(access_token=create_access_token(data.username))

@app.get("/api/products", response_model=list[ProductOutput])
def list_products(q: str = "", db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    stmt = select(Product).where(Product.active.is_(True))
    if q:
        stmt = stmt.where(Product.name.ilike(f"%{q}%") | Product.code.ilike(f"%{q}%"))
    return list(db.scalars(stmt.order_by(Product.name)).all())

@app.post("/api/products", response_model=ProductOutput, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    product = Product(**data.model_dump())
    db.add(product)
    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um produto com esse código.")

@app.post("/api/movements", response_model=MovementOutput, status_code=201)
def create_movement(data: MovementCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    product = db.scalar(select(Product).where(Product.id == data.product_id, Product.active.is_(True)).with_for_update())
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    if data.type == "SAIDA" and data.quantity > product.quantity:
        raise HTTPException(status_code=422, detail=f"Estoque insuficiente. Quantidade disponível: {product.quantity} unidades.")
    if data.type == "ENTRADA":
        product.quantity += data.quantity
    else:
        product.quantity -= data.quantity
    movement = Movement(product_id=product.id, type=data.type, quantity=data.quantity, note=data.note)
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement

@app.get("/api/products/{product_id}/movements", response_model=list[MovementOutput])
def list_movements(product_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    if db.get(Product, product_id) is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return list(db.scalars(select(Movement).where(Movement.product_id == product_id).order_by(Movement.created_at.desc())).all())

@app.get("/api/dashboard/summary", response_model=SummaryOutput)
def dashboard_summary(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    products_count = db.scalar(select(func.count(Product.id)).where(Product.active.is_(True))) or 0
    low_stock_count = db.scalar(select(func.count(Product.id)).where(Product.active.is_(True), Product.quantity <= Product.minimum_stock)) or 0
    return SummaryOutput(products_count=products_count, low_stock_count=low_stock_count)
