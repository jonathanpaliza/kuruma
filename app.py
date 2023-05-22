from fastapi import FastAPI, Request, Depends, Form, status
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    cars = db.query(models.Cars).all()
    return templates.TemplateResponse("index.html.j2", {"request": request, "cars": cars})
