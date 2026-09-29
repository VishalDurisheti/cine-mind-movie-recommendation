import ast

from model import (
    movies,
    find_movie_title,
    tfidf_matrix,
    movie_indices,
    linear_kernel
)

from query_parser import parse_query


# --------------------------------------------------
# CONVERT GENRE COLUMN INTO LIST
# --------------------------------------------------

def get_genres(value):

    try:
        return ast.literal_eval(value)

    except (ValueError, SyntaxError, TypeError):
        return []


# --------------------------------------------------
# RECOMMEND FROM NATURAL LANGUAGE
# --------------------------------------------------

def recommend_from_query(query, number_of_recommendations=10):

    parsed = parse_query(query)

    print("\nParsed query:")
    print(parsed)


    # --------------------------------------------------
    # START WITH ALL MOVIES
    # --------------------------------------------------

    candidates = movies.copy()


    # --------------------------------------------------
    # FILTER BY GENRE
    # --------------------------------------------------

    if parsed["genre"]:

        candidates = candidates[
            candidates["genres"].apply(
                lambda x: parsed["genre"] in get_genres(x)
            )
        ]


    # --------------------------------------------------
    # FILTER BY RATING
    # --------------------------------------------------

    if parsed["min_rating"] is not None:

        candidates = candidates[
            candidates["vote_average"]
            >= parsed["min_rating"]
        ]


    if parsed["max_rating"] is not None:

        candidates = candidates[
            candidates["vote_average"]
            <= parsed["max_rating"]
        ]


    # --------------------------------------------------
    # FILTER BY RUNTIME
    # --------------------------------------------------

    if parsed["max_runtime"] is not None:

        candidates = candidates[
            candidates["runtime"]
            <= parsed["max_runtime"]
        ]


    if parsed["min_runtime"] is not None:

        candidates = candidates[
            candidates["runtime"]
            >= parsed["min_runtime"]
        ]


    # --------------------------------------------------
    # FILTER BY YEAR
    # --------------------------------------------------

    if parsed["min_year"] is not None:

        candidates = candidates[
            candidates["release_year"]
            >= parsed["min_year"]
        ]


    if parsed["max_year"] is not None:

        candidates = candidates[
            candidates["release_year"]
            <= parsed["max_year"]
        ]


    # --------------------------------------------------
    # REFERENCE MOVIE
    # --------------------------------------------------

    reference_movie = parsed["reference_movie"]


    if reference_movie:

        matched_title = find_movie_title(
            reference_movie
        )

        if matched_title:

            idx = movie_indices[matched_title]

            similarity_scores = linear_kernel(
                tfidf_matrix[idx:idx + 1],
                tfidf_matrix
            ).flatten()
            # Do not recommend the movie the user already selected
            similarity_scores[idx] = -1

            movies_copy = movies.copy()

            movies_copy["similarity"] = similarity_scores

            candidates = candidates.merge(
                movies_copy[
                    ["title", "similarity"]
                ],
                on="title",
                how="left"
            )

            candidates = candidates.sort_values(
                by="similarity",
                ascending=False
            )


    else:

        # If there is no reference movie,
        # use rating and popularity.

        candidates = candidates.sort_values(
            by=["vote_average", "popularity"],
            ascending=False
        )


    # --------------------------------------------------
    # RETURN RESULTS
    # --------------------------------------------------

    return candidates[
        [
            "title",
            "genres",
            "vote_average",
            "runtime",
            "release_year"
        ]
    ].head(number_of_recommendations)


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    query = (
        "I want a sci-fi movie like Interstellar "
        "with a rating above 7 and under 180 minutes"
    )

    results = recommend_from_query(query)

    print("\n====================================")
    print("RECOMMENDATIONS")
    print("====================================")

    print(results.to_string(index=False))