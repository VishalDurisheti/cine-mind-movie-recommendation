import os
import pickle
import pandas as pd

from rapidfuzz import process, fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

DATA_PATH = "dataset/processed_movies.csv"
MODEL_DIR = "model"

TFIDF_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
MATRIX_PATH = os.path.join(MODEL_DIR, "tfidf_matrix.pkl")
MOVIES_PATH = os.path.join(MODEL_DIR, "movies.pkl")


# --------------------------------------------------
# LOAD OR BUILD MODEL
# --------------------------------------------------

if (
    os.path.exists(TFIDF_PATH)
    and os.path.exists(MATRIX_PATH)
    and os.path.exists(MOVIES_PATH)
):

    # ----------------------------------------------
    # LOAD EXISTING MODEL
    # ----------------------------------------------

    print("Loading existing model files...")

    with open(TFIDF_PATH, "rb") as file:
        tfidf = pickle.load(file)

    with open(MATRIX_PATH, "rb") as file:
        tfidf_matrix = pickle.load(file)

    with open(MOVIES_PATH, "rb") as file:
        movies = pickle.load(file)

    print("Model loaded successfully.")


else:

    # ----------------------------------------------
    # BUILD MODEL FOR THE FIRST TIME
    # ----------------------------------------------

    print("Model files not found.")
    print("Building TF-IDF model...")

    movies = pd.read_csv(DATA_PATH)

    print("Movies loaded:", len(movies))

    movies["tags"] = movies["tags"].fillna("")

    # Create TF-IDF vectorizer
    tfidf = TfidfVectorizer(
        stop_words="english"
    )

    # Convert movie tags into numerical vectors
    tfidf_matrix = tfidf.fit_transform(
        movies["tags"]
    )

    print("TF-IDF matrix shape:", tfidf_matrix.shape)

    # Create model directory if it doesn't exist
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Save TF-IDF vectorizer
    with open(TFIDF_PATH, "wb") as file:
        pickle.dump(tfidf, file)

    # Save movie data
    with open(MOVIES_PATH, "wb") as file:
        pickle.dump(movies, file)

    # Save TF-IDF matrix
    with open(MATRIX_PATH, "wb") as file:
        pickle.dump(tfidf_matrix, file)

    print("Model files saved successfully.")


# --------------------------------------------------
# CREATE MOVIE INDEX
# --------------------------------------------------

movie_indices = pd.Series(
    movies.index,
    index=movies["title"].str.lower()
).drop_duplicates()


# --------------------------------------------------
# FIND CLOSEST MOVIE TITLE
# --------------------------------------------------

def find_movie_title(user_input):

    """
    Find the closest movie title to the user's input.
    """

    user_input = user_input.lower().strip()

    titles = movies["title"].str.lower().tolist()

    result = process.extractOne(
        user_input,
        titles,
        scorer=fuzz.WRatio
    )

    if result is None:
        return None

    matched_title, score, _ = result

    # Require reasonable similarity
    if score < 70:
        return None

    return matched_title


# --------------------------------------------------
# RECOMMENDATION FUNCTION
# --------------------------------------------------

def recommend_movies(movie_title, number_of_recommendations=10):

    # Find closest matching movie
    matched_title = find_movie_title(movie_title)

    if matched_title is None:
        return []

    # Find movie index
    idx = movie_indices[matched_title]

    # Calculate similarity
    similarity_scores = linear_kernel(
        tfidf_matrix[idx:idx + 1],
        tfidf_matrix
    ).flatten()

    # Sort by similarity
    similar_indices = similarity_scores.argsort()[::-1]

    # Remove selected movie
    similar_indices = [
        i for i in similar_indices
        if i != idx
    ]

    # Get top recommendations
    top_indices = similar_indices[
        :number_of_recommendations
    ]

    recommendations = movies.iloc[top_indices][
        [
            "title",
            "genres",
            "vote_average",
            "release_year"
        ]
    ]

    return recommendations


# --------------------------------------------------
# TEST THE MODEL
# --------------------------------------------------

if __name__ == "__main__":

    movie = "inter stellar"

    recommendations = recommend_movies(
        movie,
        10
    )

    print("\n===================================")
    print("MOVIE RECOMMENDATIONS")
    print("===================================")

    print(f"\nBecause you liked: {movie}\n")

    if len(recommendations) == 0:

        print("Movie not found.")

    else:

        for index, row in recommendations.iterrows():

            print(
                f"{row['title']} | "
                f"Rating: {row['vote_average']} | "
                f"Year: {row['release_year']}"
            )