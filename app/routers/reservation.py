from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.reservation import ReservationCreate, ReservationOut
from app.models.reservation import Reservation
from app.services.reservation_service import create_reservation

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ReservationOut])
def list_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

@router.post("/", response_model=ReservationOut)
def create_reservation_api(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return create_reservation(db, reservation)

@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_res = db.query(Reservation).get(reservation_id)
    db.delete(db_res)
    db.commit()
    return {"ok": True}
