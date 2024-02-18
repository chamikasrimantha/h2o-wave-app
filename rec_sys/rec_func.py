import pickle
from .movie import Movie
import numpy as np
from typing import List

class Recommender:
    def __init__(self):
        """
        Creates an instance of the recommender system after loading the data.
        """
        self.rating_matrix = pickle.load(
            open("rec_sys/rec_data/rating_matrix.pkl", "rb")
        )
        self.movies = pickle.load(open("rec_sys/rec_data/movies.pkl", "rb"))
        self.similarity_scores = pickle.load(
            open("rec_sys/rec_data/similarity_scores.pkl", "rb")
        )
        self.movie_names = pickle.load(open("rec_sys/rec_data/movie_names.pkl", "rb"))

    def recommend(self, movie_name: str) -> List[Movie]:
        """
        Find similar movies to the given movie name.
        Parameters:
            movie_name: str - name of the movie.
        If the movie is not found an exception will be raised.
        Returns:
            list of movies.
        """
        movie_idx = np.where(self.rating_matrix.index == movie_name)[0][0]
        similar_items = list(enumerate(self.similarity_scores[movie_idx]))
        similar_items.sort(reverse=True, key=lambda x: x[1])

        recommended_movies = []
        for i in similar_items[1:6]:
            movie_match_df = self.movies[
                self.movies["Title"] == self.rating_matrix.index[i[0]]
            ].drop_duplicates("Title")

            movie = Movie(
                movie_match_df["Title"].values[0],
                movie_match_df["Director"].values[0],
                movie_match_df["Release_Year"].values[0],
                movie_match_df["Genre"].values[0],
                movie_match_df["Rating"].values[0],
                movie_match_df["Poster"].values[0],
            )
            recommended_movies.append(movie)

        return recommended_movies


recommender = Recommender()