from sqlalchemy import Column, Integer, String
from database import Base


class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    model = Column(String)
    make = Column(String)
    year = Column(Integer)

