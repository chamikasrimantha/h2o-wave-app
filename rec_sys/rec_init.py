import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple


def read_dataset() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read the datasets.
    Returns:
        tuple containing DataFrames for movies and ratings
    """
    movies = pd.read_csv("rec_sys/dataset/Movies.csv", low_memory=False)
    ratings = pd.read_csv("rec_sys/dataset/Ratings.csv")

    return movies, ratings


def save_data(rating_matrix, similarity_scores, movies):
    """
    Saves rating matrix, movies, movie names, and similarity scores in pickle format.
    Parameters:
        rating_matrix: pandas.DataFrame - User rating for each movie
        similarity_scores: 
        movies: pandas.DataFrame - Details of the movies
    """
    pickle.dump(
        list(rating_matrix.index), open("rec_sys/rec_data/movie_names.pkl", "wb")
    )
    pickle.dump(rating_matrix, open("rec_sys/rec_data/movies.pkl", "wb"))
    pickle.dump(movies, open("rec_sys/rec_data/movies.pkl", "wb"))
    pickle.dump(similarity_scores, open("rec_sys/rec_data/similarity_scores.pkl", "wb"))


def rec_init():
    """
    Computes the similarity scores based on collaborative filtering.
    Users that reviewed more than 200 movies and movies with equal or more than 50 ratings 
    are considered to improve the quality of recommendations. Similarity is measured based
    on cosine-similarity.
    """
    movies, ratings = read_dataset()

    ratings_with_movies = ratings.merge(movies, on="Movie-ID")

    # Finding users with more than 200 reviews.
    ratings_group = ratings_with_movies.groupby("User-ID").count()["Rating"]
    ratings_group = ratings_group[ratings_group > 200]

    ratings_filtered = ratings_with_movies[
        ratings_with_movies["User-ID"].isin(ratings_group.index)
    ]

    # Finding movies with equal or more than 50 ratings.
    filtered_group = ratings_filtered.groupby("Title").count()["Rating"]
    filtered_group = filtered_group[filtered_group >= 50]

    final_filtered_ratings = ratings_filtered[
        ratings_filtered["Title"].isin(filtered_group.index)
    ]

    rating_matrix = final_filtered_ratings.pivot_table(
        index="Title", columns="User-ID", values="Rating"
    )
    rating_matrix.fillna(0, inplace=True)

    similarity_scores = cosine_similarity(rating_matrix)
    save_data(rating_matrix, similarity_scores, movies)


if __name__ == "__main__":
    rec_init()
    