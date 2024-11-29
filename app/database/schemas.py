from pydantic import BaseModel
from typing import List


class Purchase(BaseModel):
    id: int
    item: str
    price: float


class UserResponse(BaseModel):
    name: str
    email: str
    purchases: List[Purchase]


class Report(BaseModel):
    id: int
    title: str
    status: str


class AdminResponse(BaseModel):
    name: str
    email: str
    reports: List[Report]
