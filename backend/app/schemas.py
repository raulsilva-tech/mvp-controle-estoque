from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class LoginInput(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)

class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProductCreate(BaseModel):
    code: str = Field(min_length=1, max_length=30)
    name: str = Field(min_length=1, max_length=150)
    category: str = Field(default="", max_length=80)
    quantity: int = Field(default=0, ge=0)
    minimum_stock: int = Field(default=0, ge=0)

class ProductOutput(BaseModel):
    id: int
    code: str
    name: str
    category: str
    quantity: int
    minimum_stock: int
    active: bool
    model_config = ConfigDict(from_attributes=True)

class MovementCreate(BaseModel):
    product_id: int
    type: Literal["ENTRADA", "SAIDA"]
    quantity: int = Field(gt=0)
    note: str = Field(default="", max_length=250)

class MovementOutput(BaseModel):
    id: int
    product_id: int
    type: str
    quantity: int
    note: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SummaryOutput(BaseModel):
    products_count: int
    low_stock_count: int
