# usecases.py

import logging
import re
import pandas as pd
import io
from app.repositories import movies

def get_intervals():
    try:
        return movies.get_movies_interval()
    except Exception as e:
        return {"error": str(e)}

def upload_csv(file_contents: bytes):
    try:
    
        df = pd.read_csv(io.StringIO(file_contents.decode()), delimiter=";")

        producers_count = {}

        logging.info("UPLOAD CSV - START")

        for _, row in df.iterrows():
            is_winner =  True if row["winner"] == "yes" and "winner" in row else False
            if is_winner:
                year = row["year"]
                producers = row["producers"].strip()
                key = re.split(r',| and ', producers)
                
                for k in key:
                    if k not in producers_count:
                        producers_count[k] = {"years": [year]}
                    else:
                        producers_count[k]["years"].append(year)

        producers_winners = []
        for key, value in producers_count.items():
            if len(value["years"]) > 1:
                producer = key
                years = value["years"]
                first_win = min(years)
                last_win = max(years)
                producers_winners.append({'producer': producer, 'interval' : (last_win - first_win), 
                                          'previousWin': first_win, 'followingWin': last_win})

        max_min_winners = {}
        min_interval = 9999
        max_interval = 0

        for producer in producers_winners:
            if producer['interval'] < min_interval:
                min_interval = producer['interval']
                max_min_winners['min'] = producer
            if producer['interval'] > max_interval:
                max_interval = producer['interval']
                max_min_winners['max'] = producer

        if len(max_min_winners) > 0:
            movies.insert_movies_database(max_min_winners)
        else:
            logging.info("UPLOAD CSV - NO RESULTS")    

        logging.info("UPLOAD CSV - END")

        return max_min_winners

    except Exception as e:
        return {"error": str(e)}