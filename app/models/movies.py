from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base, engine

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    producer = Column(String)
    interval = Column(Integer)
    previousWin = Column(Integer)
    followingWin = Column(Integer)
    min = Column(Boolean)

Base.metadata.create_all(bind=engine)