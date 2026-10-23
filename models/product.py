from pydantic import BaseModel
from enums.status import Status
from enums.departments import Department
class ProductBase(BaseModel):
    name: str
    starting_price: int
    finish_price: int
    description: str
    department: Department = Department.others
    category: str
    status : Status

class ProductID(ProductBase):
    id: int




