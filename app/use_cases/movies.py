# usecases.py

import io
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from models import Movie
from db.database import DATABASE_URL
from repositories import movies

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_intervals():
    try:
        return movies.get_movies_interval()
    except Exception as e:
        return {"error": str(e)}


def upload_csv(session: Session, file_contents: bytes):
    try:
        df = pd.read_csv(io.StringIO(file_contents.decode("utf-8")), delimiter=";")

        for _, row in df.iterrows():
            is_winner = row["winner"] == "yes" if "winner" in row else False
            movie_data = Movie(
                year=row["year"],
                title=row["title"],
                studios=row["studios"],
                producers=row["producers"],
                winner=is_winner,
            )
            session.add(movie_data)
        session.commit()

        return {"message": "Arquivo CSV importado com sucesso."}

    except Exception as e:
        return {"error": str(e)}