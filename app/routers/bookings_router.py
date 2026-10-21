from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Booking, Pass, User
from app.schemas import BookingCreate, BookingResponse
from app.routers.auth_router import get_current_user

try:
    from app.utils.whatsapp import send_whatsapp_ticket
except Exception:
    def send_whatsapp_ticket(phone_number, ticket_details):
        return None

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=List[BookingResponse])
def create_booking(booking_data: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pass_obj = db.query(Pass).filter(Pass.id == booking_data.pass_id).first()
    if not pass_obj:
        raise HTTPException(status_code=404, detail="Pass not found")
    
    if pass_obj.available_quantity < booking_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough passes available")
    
    pass_obj.available_quantity -= booking_data.quantity
    
    created_bookings = []
    for attendee in booking_data.attendees:
        db_booking = Booking(
            user_id=current_user.id,
            pass_id=pass_obj.id,
            attendee_name=attendee.name,
            attendee_gender=attendee.gender,
            attendee_phone=attendee.phone
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        created_bookings.append(db_booking)
        
        # Try sending whatsapp notification safely
        try:
            ticket_info = f"NAVRATRI 2026 Ticket Confirmed! Pass: {pass_obj.name}, Name: {attendee.name}, ID: {db_booking.ticket_code}"
            send_whatsapp_ticket(attendee.phone, ticket_info)
        except Exception:
            pass

    return created_bookings

@router.get("/my", response_model=List[BookingResponse])
def get_my_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Booking).filter(Booking.user_id == current_user.id).all()