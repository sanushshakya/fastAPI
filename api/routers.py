#FastAPI imports
from fastapi import APIRouter, Body, Request, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#Model imports
from api.model import ProductModel, UpdateProductModel

#Config import 
from config import settings

products = []

#Defining our api routers
def get_api_router(app):
    #create FAST API router
    router = APIRouter()

    #define a root path for our API with metadata
    @router.get("/", response_description= "API MetaData")
    async def api_metadata(request: Request):
        result = {
            "api": "API",
            "author": "Sanush Shakya",
            "website": "#",
            "email": "shakyasanush7@gmail.com",
            "version": "1.0"
        }

        return JSONResponse(status_code=status.HTTP_200_OK, content=result)

    #return a list of product
    @router.get("/products", response_description="List Products")
    async def list_products(request: Request):
        return JSONResponse(status_code=status.HTTP_200_OK, content=products)

    #create a new task
    @router.post("/products", response_description="Add Products")
    async def add_product(request: Request, product: ProductModel = Body(...)):
        #encode our product with json
        create_product = jsonable_encoder(product)
        #insert a new product
        products.append(create_product)
        #return a success message
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=create_product)

    #allows to get a product
    @router.get("/product/{id}", response_description="Get Product")
    async def get_product(id: str, request: Request):
        #find and return product
        for product in products:
            if product['_id'] == id:
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=product)
            #return error if not found
            raise HTTPException(status_code=404, detail=f"Product {id} not found")

    #allows to update a product
    @router.put("/product/{id}", response_description="Update Product")
    async def update_product(id: str, request: Request, product: UpdateProductModel = Body(...)):
        #encode our product with json
        new_product = jsonable_encoder(product)
        new_product['_id'] = id
        #find and update the product
        for product in products:
            if product['_id'] == id:
                products.remove(product)
                products.append(new_product)
                return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_product)
        #return error if not found
            raise HTTPException(status_code=404, detail=f"Product {id} not found")

    #allows to delete a product
    @router.delete("/product/{id}", response_description="Delete Product")
    async def update_product(id: str, request: Request):
        #find and delete the product
        for product in products:
            if product['_id'] == id:
                products.remove(product)
                return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        #return error if not found
            raise HTTPException(status_code=404, detail=f"Product {id} not found")

    #return our router
    return router

