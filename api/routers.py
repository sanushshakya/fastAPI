#FastAPI imports
from fastapi import APIRouter, Body, Request, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#Model imports
from api.model import ProductModel, UpdateProductModel

#Config import 
from config import settings

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
        products = []
        for doc in await request.app.mongodb["products"].find.to_list(length=100):
            products.append(doc)
        return JSONResponse(status_code=status.HTTP_200_OK, content=products)

    #create a new task
    @router.post("/products", response_description="Add Products")
    async def add_product(request: Request, product: ProductModel = Body(...)):
        #encode our product with json
        product = jsonable_encoder(product)
        #insert a new product
        new_product = await request.app.mongodb["products"].insert_one(product)
        created_product = await request.app.mongodb["products"].find_one(
            {
            "_id": new_product.inserted_id
            }
        )
        #return a success message
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_product)

    #allows to get a product
    @router.get("/product/{id}", response_description="Get Product")
    async def get_product(id: str, request: Request):
        #find and return product
        if (product := await request.app.mongodb["product"].find_one({"_id": id})) is not None:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=product)
        #return error if not found
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    #allows to update a product
    @router.put("/product/{id}", response_description="Update Product")
    async def update_product(id: str, request: Request, product: UpdateProductModel = Body(...)):
        product = {k: v for k, v in product.dict().items() if v is not None }
        if len(product) >= 1:
                update_result = await request.app.mongodb["product"].update_one(
                    {"_id":id},{"$set": product}
                )
                if update_result.modified_count == 1:
                    if (
                        updated_product := await request.app.mongodb["product"].find_one(
                        {"_id": id}
                        ) 
                    )is not None:
                        return JSONResponse(status_code=status.HTTP_201_CREATED, content=updated_product)
        if  (
            existing_product := await request.app.mongodb["product"].find_one({"_id": id})
        )  is not None:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=updated_product)
        #return error if not found
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    #allows to delete a product
    @router.delete("/product/{id}", response_description="Delete Product")
    async def update_product(id: str, request: Request):
        #find and delete the product
        delete_result = await request.app.mongodb["product"].delete_one({"_id": id})
        if delete_result.deleted_count == 1:
                return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        #return error if not found
        raise HTTPException(status_code=404, detail=f"Product {id} not found")

    #return our router
    return router

