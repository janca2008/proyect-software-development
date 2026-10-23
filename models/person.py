from pydantic import BaseModel, EmailStr
from enums.id_type import IdType


class PersonBase(BaseModel):
    first_name: str
    last_name: str
    id_type: IdType
    id_number: str
    phone_number: str
    email: EmailStr


class CustomerBase(PersonBase):
    address: str


class CustomerID(CustomerBase):
    id: int


class WorkerBase(PersonBase):
    position: str


class WorkerID(WorkerBase):
    id: int