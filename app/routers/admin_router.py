from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Ticket, Booking, Pass
from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

def check_admin(user: User = Depends(get_current_user)):
    if user.role.value != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    total_bookings = db.query(Booking).count()
    total_tickets_sold = db.query(Ticket).count()
    
    all_bookings = db.query(Booking).all()
    total_revenue = sum(b.total_amount for b in all_bookings) if all_bookings else 0.0
    
    all_tickets = db.query(Ticket).all()
    checked_in_count = sum(1 for t in all_tickets if str(t.status).lower() in ['checked_in', 'checked-in', 'used'])

    male_count = sum(1 for t in all_tickets if str(t.attendee_gender).strip().lower() == 'male')
    female_count = sum(1 for t in all_tickets if str(t.attendee_gender).strip().lower() == 'female')
    other_count = total_tickets_sold - (male_count + female_count)

    return {
        "total_bookings": total_bookings,
        "total_tickets_sold": total_tickets_sold,
        "total_revenue": total_revenue,
        "checked_in_count": checked_in_count,
        "gender_stats": {
            "male": male_count,
            "female": female_count,
            "other": other_count
        }
    }

@router.get("/bookings")
def get_all_bookings(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    bookings = db.query(Booking).all()
    res = []
    for b in bookings:
        pass_obj = db.query(Pass).filter(Pass.id == b.pass_id).first()
        user_obj = db.query(User).filter(User.id == b.user_id).first()
        tickets = db.query(Ticket).filter(Ticket.booking_id == b.id).all()
        
        res.append({
            "booking_id": str(b.id),
            "user_name": user_obj.name if user_obj else "Unknown",
            "user_email": user_obj.email if user_obj else "N/A",
            "pass_title": pass_obj.title if pass_obj else "N/A",
            "total_amount": b.total_amount,
            "created_at": b.created_at.strftime("%Y-%m-%d %H:%M"),
            "attendees": [
                {
                    "name": t.attendee_name,
                    "gender": t.attendee_gender,
                    "phone": t.attendee_phone,
                    "qr_token": t.qr_token,
                    "status": str(t.status)
                } for t in tickets
            ]
        })
    return res

@router.post("/tickets/scan")
def scan_ticket(
    payload: dict,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    qr_token = payload.get("qr_token")
    if not qr_token:
        raise HTTPException(status_code=400, detail="QR token required")
    
    ticket = db.query(Ticket).filter(Ticket.qr_token == qr_token).first()
    if not ticket:
        return {"status": "INVALID", "message": "Invalid QR Token. Ticket not found!"}
    
    if str(ticket.status).lower() in ['checked_in', 'checked-in', 'used']:
        return {"status": "ALREADY_USED", "message": f"Ticket ALREADY USED by {ticket.attendee_name}!"}
    
    from datetime import datetime
    ticket.status = "CHECKED_IN"
    ticket.checked_in_at = datetime.utcnow()
    db.commit()
    
    return {
        "status": "VALID",
        "message": "Entry Verified Successfully!",
        "attendee_name": ticket.attendee_name,
        "attendee_gender": ticket.attendee_gender
    }