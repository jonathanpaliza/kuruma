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


@app.post("/add_car")
async def add_car(request: Request, make: Annotated[str, Form()], model: Annotated[str, Form()], year: Annotated[int, Form()], db: Annotated[Session, Depends(get_db)]):
    add_car = models.Cars(make=make, model=model, year=year)
    db.add(add_car)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/cars")
async def list_car(request: Request, db: Annotated[Session, Depends(get_db)]):
    cars = db.query(models.Cars).all()
    return templates.TemplateResponse("cars.html.j2", {"request": request, "cars": cars})


@app.get("/delete/{car_id}")
async def delete_car(request: Request, car_id: int, db: Annotated[Session, Depends(get_db)]):
    cars = db.query(models.Cars).filter(models.Cars.id == car_id).first()
    db.delete(cars)
    db.commit()

    url = app.url_path_for("list_car")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

