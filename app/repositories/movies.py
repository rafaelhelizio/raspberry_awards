from sqlalchemy import func
from app.db.database import SessionLocal
from models import Movie

def get_movies_interval():

    db = SessionLocal()

    producers = (
        db.query(Movie.producers)
        .filter(Movie.winner)
        .group_by(Movie.producers)
        .having(func.count(Movie.year) > 1)
        .all()
    )

    results = {"min": [], "max": []}

    for producer in producers:
        producer_name = producer[0]
        intervals = (
            db.query(Movie.year)
            .filter(Movie.winner, Movie.producers == producer_name)
            .order_by(Movie.year)
            .all()
        )

        min_interval = None
        max_interval = None
        previous_win = None

        for year in intervals:
            if previous_win is None:
                previous_win = year[0]
            else:
                interval = year[0] - previous_win
                if max_interval is None or interval > max_interval:
                    max_interval = interval
                if min_interval is None or interval < min_interval:
                    min_interval = interval
                previous_win = year[0]

        if min_interval is not None and max_interval is not None:
            producer_info = {
                "producer": producer_name,
                "interval": min_interval if min_interval == max_interval else max_interval,
                "previousWin": previous_win - max_interval,
                "followingWin": previous_win,
            }
            results["min" if min_interval == max_interval else "max"].append(producer_info)

    db.close()

    return results