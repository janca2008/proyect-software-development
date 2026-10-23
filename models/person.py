from pydantic import BaseModel
from enums.id_type import IdType
from enums.status import Status


class PersonBase(BaseModel):
    first_name: str
    last_name: str
    id_type: IdType
    id_number: str
    phone_number: str
    email: str
    status: Status


class CustomerBase(PersonBase):
    address: str


class CustomerID(CustomerBase):
    id: int


class WorkerBase(PersonBase):
    position: str


class WorkerID(WorkerBase):
    id: int