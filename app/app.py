from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from pydantic import BaseModel

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
async def companies_get(
    db: Session = Depends(get_db),
):
    count = db.query(Company).count()
    return {"count": count}


class CompanySchema(BaseModel):
    name: str


@app.post("/companies")
def companies_post(
    company: CompanySchema,
    db: Session = Depends(get_db),
):
    company = Company(name=company.name)
    db.add(company)
    db.commit()
    return "inserted"
