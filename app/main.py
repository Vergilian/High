from fastapi import FastAPI
from app.routers import table, reservation
from app.db.database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(table.router, prefix="/tables", tags=["tables"])
app.include_router(reservation.router, prefix="/reservations", tags=["reservations"])
