from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Company

app = FastAPI()


@app.get("/")
async def root(
    db: Session = Depends(get_db),
):
    count = db.execute("select 1 + 1").scalar()
    return {"message": count}


@app.get("/companies")
async def companies(
    db: Session = Depends(get_db),
):
    count = db.query(Company).count()
    return {"count": count}
