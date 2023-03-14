from pydantic import BaseModel, Field
import uuid

class ProductModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    price: int = Field(...)
     
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "Haiku",
                "description": "This is haiku product.",
                "price": 500
            }
        }

class UpdateProductModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    price: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Haiku",
                "description": "This is haiku product.",
                "price": 500
            }
        }