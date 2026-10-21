import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class RoleEnum(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"

class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class TicketStatusEnum(str, enum.Enum):
    VALID = "VALID"
    USED = "USED"
    CANCELLED = "CANCELLED"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.CUSTOMER)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user")

class Pass(Base):
    __tablename__ = "passes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    total_quantity = Column(Integer, nullable=False)
    remaining_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="pass_item")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    pass_id = Column(String, ForeignKey("passes.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="CONFIRMED")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    pass_item = relationship("Pass", back_populates="bookings")
    tickets = relationship("Ticket", back_populates="booking", cascade="all, delete-orphan")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False)
    attendee_name = Column(String, nullable=False)
    attendee_gender = Column(String, nullable=False)
    attendee_phone = Column(String, nullable=True)
    qr_token = Column(String, unique=True, index=True, nullable=False)
    status = Column(Enum(TicketStatusEnum), default=TicketStatusEnum.VALID)
    checked_in_at = Column(DateTime, nullable=True)

    booking = relationship("Booking", back_populates="tickets")