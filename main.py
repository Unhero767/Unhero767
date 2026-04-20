from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import SessionLocal, TableA, Sovereign, init_db
import datetime

# Initialize the Lithic Substrate and Identity Layer
init_db()

app = FastAPI(title="MLAOS Sovereign Substrate")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/start_transaction")
async def start_transaction(db: Session = Depends(get_db)):
    # 1. Sovereign Identity Ritual
    hero = db.query(Sovereign).filter(Sovereign.handle == "HeroUnhero").first()
    if not hero:
        hero = Sovereign(
            handle="HeroUnhero", 
            clearance_tier=1, 
            empathy_baseline=100,
            last_manifestation=datetime.datetime.utcnow()
        )
        db.add(hero)
        db.commit()
        db.refresh(hero)

    # 2. Baseline Record Ritual
    record = db.query(TableA).filter(TableA.id == 3).first()
    if not record:
        record = TableA(id=3, value="baseline_value", integrity_score=100)
        db.add(record)
        db.commit()

    return {
        "status": "success", 
        "sovereign": hero.handle, 
        "tier": hero.clearance_tier,
        "state": "◦A_INIT"
    }

@app.post("/simulate_failure")
async def simulate_failure(db: Session = Depends(get_db)):
    try:
        db.execute(text("UPDATE table_a SET value='corrupted' WHERE id=3"))
        raise Exception("Intentional Metalogical Burn.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health(db: Session = Depends(get_db)):
    record = db.query(TableA).filter(TableA.id == 3).first()
    hero = db.query(Sovereign).filter(Sovereign.handle == "HeroUnhero").first()
    return {
        "status": "STABLE",
        "sovereign_active": hero.handle if hero else "NONE",
        "current_value": record.value if record else "NULL",
        "integrity": record.integrity_score if record else 0
    }
