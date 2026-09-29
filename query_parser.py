import re


# --------------------------------------------------
# GENRE KEYWORDS
# --------------------------------------------------

GENRE_MAP = {
    "sci-fi": "Science Fiction",
    "science fiction": "Science Fiction",
    "scifi": "Science Fiction",
    "action": "Action",
    "comedy": "Comedy",
    "drama": "Drama",
    "horror": "Horror",
    "romance": "Romance",
    "thriller": "Thriller",
    "animation": "Animation",
    "adventure": "Adventure",
    "fantasy": "Fantasy",
    "crime": "Crime",
    "mystery": "Mystery",
    "documentary": "Documentary",
    "family": "Family",
    "war": "War",
    "western": "Western",
    "music": "Music",
}


# --------------------------------------------------
# PARSE USER QUERY
# --------------------------------------------------

def parse_query(query):

    query_lower = query.lower()

    result = {
        "genre": None,
        "min_rating": None,
        "max_rating": None,
        "min_runtime": None,
        "max_runtime": None,
        "min_year": None,
        "max_year": None,
        "reference_movie": None
    }


    # --------------------------------------------------
    # 1. FIND GENRE
    # --------------------------------------------------

    for keyword, genre in GENRE_MAP.items():

        if keyword in query_lower:

            result["genre"] = genre
            break


    # --------------------------------------------------
    # 2. FIND RATING
    # --------------------------------------------------

    # Minimum rating
    min_rating_patterns = [
        r"(?:rating\s*)?(?:above|over|greater than|at least)\s*(\d+(?:\.\d+)?)",
        r"(\d+(?:\.\d+)?)\s*(?:or higher|and above)\s*(?:rating|stars?)"
    ]

    for pattern in min_rating_patterns:

        match = re.search(pattern, query_lower)

        if match:
            result["min_rating"] = float(match.group(1))
            break


    # Maximum rating
    max_rating_patterns = [
        r"(?:rating\s*)?(?:below|less than|up to)\s*(\d+(?:\.\d+)?)\s*(?:rating|stars?)",
        r"(\d+(?:\.\d+)?)\s*(?:or lower|and below)\s*(?:rating|stars?)"
    ]

    for pattern in max_rating_patterns:

        match = re.search(pattern, query_lower)

        if match:
            result["max_rating"] = float(match.group(1))
            break
    
    # --------------------------------------------------
    # 3. FIND RUNTIME
    # --------------------------------------------------

    runtime_under = re.search(
        r"(?:under|less than|below|shorter than)\s*(\d+)\s*(?:minutes|min)",
        query_lower
    )

    if runtime_under:

        result["max_runtime"] = int(
            runtime_under.group(1)
        )


    runtime_over = re.search(
        r"(?:over|more than|above|longer than)\s*(\d+)\s*(?:minutes|min)",
        query_lower
    )

    if runtime_over:

        result["min_runtime"] = int(
            runtime_over.group(1)
        )


    # --------------------------------------------------
    # 4. FIND RELEASE YEAR
    # --------------------------------------------------

    year_after = re.search(
        r"(?:after|from|since|newer than)\s*(19\d{2}|20\d{2})",
        query_lower
    )

    if year_after:

        result["min_year"] = int(
            year_after.group(1)
        )


    year_before = re.search(
        r"(?:before|older than)\s*(19\d{2}|20\d{2})",
        query_lower
    )

    if year_before:

        result["max_year"] = int(
            year_before.group(1)
        )


    # --------------------------------------------------
    # 5. FIND REFERENCE MOVIE
    # --------------------------------------------------

    like_match = re.search(
        r"(?:like|similar to|similar)\s+(.+?)(?:\s+with|\s+above|\s+below|\s+under|\s+over|$)",
        query_lower
    )

    if like_match:

        result["reference_movie"] = (
            like_match.group(1)
            .strip()
        )


    return result


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    query = (
        "I want a sci-fi movie like Interstellar "
        "with a rating above 8 and under 150 minutes"
    )

    result = parse_query(query)

    print("User query:")
    print(query)

    print("\nParsed query:")
    print(result)