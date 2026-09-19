from datetime import date, time

from pydantic import BaseModel, EmailStr, Field

class BookingCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    date: date

    time: time

class BookingResponse(BaseModel):
   
    id: int
    name: str
    email: EmailStr
    date: date
    time: time

    model_config = {
        "from_attributes": True,
    }