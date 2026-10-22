from fastapi import APIRouter

router = (APIRouter)

@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/")
async def say_hello(name: str):
    return {"message": f"hola{name}"}