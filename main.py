from fastapi import FastAPI
from routers import product
app = FastAPI()


app.include_router(router=product.router, prefix="/product", tags=["product"])
