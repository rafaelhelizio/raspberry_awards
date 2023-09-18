from app.db.database import Session
from app.models import Movie
from app.schema.movies import Winners, WinnersResponse

def get_movies_interval() -> WinnersResponse:
    with Session() as session:
        result = session.query(Movie).all()

        min_movie = None
        max_movie = None

        for r in result:
            data_set = movie_to_winners(r)
            if r.min:
                min_movie = data_set
            else:
                max_movie = data_set

        if min_movie is None:
            min_movie = {"producer": "Unknown", "interval": 0, "previousWin": 0, "followingWin": 0}

        if max_movie is None:
            max_movie = {"producer": "Unknown", "interval": 0, "previousWin": 0, "followingWin": 0}

        response = WinnersResponse(min=min_movie, max=max_movie)

        return response

def movie_to_winners(movie: Movie) -> Winners:
    return Winners(
        producer=movie.producer,
        interval=movie.interval,
        previousWin=movie.previousWin,
        followingWin=movie.followingWin,
    )

def insert_movies_database(max_min_winners):
    try:
        
        db = Session()

        all_movies = db.query(Movie).all()
        
        if len(all_movies) > 0:
            db.query(Movie).delete()
            db.commit()

        for key in max_min_winners:
            rec_data = {
                        "producer": max_min_winners[key]['producer'],
                        "interval": max_min_winners[key]['interval'],
                        "previousWin": max_min_winners[key]['previousWin'],
                        "followingWin": max_min_winners[key]['followingWin'],
                        "min": True if key == 'min' else False,
                    }
            awards = Movie(**rec_data)
            if len(all_movies) > 0:            
                for movie in all_movies:
                    if movie.min == True and key == 'min' and max_min_winners[key]['interval'] > movie.interval:
                        awards.producer = movie.producer
                        awards.interval = movie.interval
                        awards.previousWin = movie.previousWin
                        awards.followingWin = movie.followingWin
                        awards.min = movie.min
                    if movie.min == False and key == 'max' and max_min_winners[key]['interval'] < movie.interval:
                        awards.producer = movie.producer
                        awards.interval = movie.interval
                        awards.previousWin = movie.previousWin
                        awards.followingWin = movie.followingWin
                        awards.min = movie.min

            db.add(awards)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            return False
        

        all_movies = db.query(Movie).all()
        movies = all_movies

        db.close()



        return True
    except Exception as e:
        db.rollback()
        return {"error": str(e)}