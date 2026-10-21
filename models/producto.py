from pydantic import BaseModel

class productoBase(BaseModel):
    name: str
    starting_price: int
    finish_price: int
    utility : int #TODO calcular la resta de finish price y starting price
    description: str
    department: str
    category: str
    status : str #TODO hacer un enums para activate y deactivate





