from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.table import Table
from app.schemas.table import TableCreate, TableOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[TableOut])
def list_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()

@router.post("/", response_model=TableOut)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    db_table = db.query(Table).get(table_id)
    db.delete(db_table)
    db.commit()
    return {"ok": True}
