from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- Auth Schemas ---
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str
    gender: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_name: str

# --- Pass Schemas ---
class PassCreate(BaseModel):
    title: str
    price: float
    total_quantity: int
    date: str
    venue: str

class PassResponse(PassCreate):
    id: str
    remaining_quantity: int

    class Config:
        from_attributes = True

# --- Booking & Attendee Schemas ---
class AttendeeCreate(BaseModel):
    name: str
    gender: str
    phone: str

class BookingCreate(BaseModel):
    pass_id: str
    attendees: List[AttendeeCreate]

class TicketResponse(BaseModel):
    id: str
    attendee_name: str
    attendee_gender: str
    attendee_phone: Optional[str] = None
    qr_token: str
    status: str

    class Config:
        from_attributes = True
class BookingResponse(BaseModel):
    id: int
    user_id: int
    pass_id: int
    attendee_name: str
    attendee_gender: str = None
    attendee_phone: str = None
    ticket_code: str = None

    class Config:
        from_attributes = True
