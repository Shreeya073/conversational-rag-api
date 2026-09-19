from datetime import date as DateType
from datetime import time as TimeType
from pydantic import BaseModel, EmailStr

class BookingExtraction(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    date: DateType | None = None
    time: TimeType | None = None