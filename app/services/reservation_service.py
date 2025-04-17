from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

def create_reservation(db: Session, reservation: ReservationCreate):
    start = reservation.reservation_time
    end = start + timedelta(minutes=reservation.duration_minutes)
    conflicts = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id,
        Reservation.reservation_time < end,
        (Reservation.reservation_time + timedelta(minutes=Reservation.duration_minutes)) > start
    ).first()
    if conflicts:
        raise HTTPException(status_code=400, detail="Table already booked for this time slot.")
    new_reservation = Reservation(**reservation.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation
