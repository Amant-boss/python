from http.client import HTTPException

import database
import main
from main import Movie, MovieCreate
from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome"}

@app.post("/movies/", response_model=Movie)
def create_movie(movie: MovieCreate):
   movie_id = database.create_movie(movie)
   return models.Movie(id = movie_id, **movie.dict())

@app.get("/movies/" , response_model=Movie)
def read_movie(movie_id ,  int):
    movie = database.read_movies(movie_id)
    if movie is None:
        raise HTTPException(status_code= 404 , detail="Movie Not Found")
    return movie