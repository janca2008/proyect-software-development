from fastapi import FastAPI
from routers import product, customer, worker
app = FastAPI()

app.include_router(router=product.router, prefix="/product", tags=["product"])
app.include_router(router=customer.router, prefix="/customer", tags=["customer"])
app.include_router(router=worker.router, prefix="/worker", tags=["worker"])