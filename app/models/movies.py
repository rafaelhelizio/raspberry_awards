from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    title = Column(String, index=True)
    studios = Column(String)
    producers = Column(String)
    winner = Column(Boolean, default=False)
