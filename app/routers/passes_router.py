from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Pass, User, RoleEnum
from app.schemas import PassResponse, PassCreate
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/v1/passes", tags=["Passes"])

@router.get("", response_model=List[PassResponse])
def get_all_passes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    passes = db.query(Pass).all()
    return passes

@router.post("", response_model=PassResponse)
def create_pass(pass_data: PassCreate, db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    new_pass = Pass(
        title=pass_data.title,
        price=pass_data.price,
        date=pass_data.date,
        venue=pass_data.venue,
        total_quantity=pass_data.total_quantity,
        remaining_quantity=pass_data.total_quantity
    )
    db.add(new_pass)
    db.commit()
    db.refresh(new_pass)
    return new_pass