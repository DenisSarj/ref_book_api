from pydantic import BaseModel
from typing import List


class PhoneNumberResponse(BaseModel):
    number: str

    class Config:
        orm_mode = True
        from_attributes = True


class OrganizationBase(BaseModel):
    id: int
    name: str
    building_id: int
    activity_id: int
    phone_numbers: List[PhoneNumberResponse]

    class Config:
        orm_mode = True
        from_attributes = True


class OrganizationsResponse(BaseModel):
    organizations: List[OrganizationBase]
