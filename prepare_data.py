import pandas as pd
import ast


# --------------------------------------------------
# 1. LOAD DATASETS
# --------------------------------------------------

movies = pd.read_csv("dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb_5000_credits.csv")

print("Movies:", movies.shape)
print("Credits:", credits.shape)


# --------------------------------------------------
# 2. MERGE DATASETS
# --------------------------------------------------

movies = movies.merge(
    credits,
    left_on="id",
    right_on="movie_id"
)

print("After merging:", movies.shape)


# --------------------------------------------------
# 3. SELECT IMPORTANT COLUMNS
# --------------------------------------------------

movies = movies[
    [
        "title_x",
        "genres",
        "keywords",
        "overview",
        "cast",
        "crew",
        "vote_average",
        "vote_count",
        "runtime",
        "release_date",
        "popularity"
    ]
]


# Rename title_x to title
movies.rename(columns={"title_x": "title"}, inplace=True)


# --------------------------------------------------
# 4. CONVERT JSON-LIKE TEXT INTO LISTS
# --------------------------------------------------

def extract_names(text):
    """
    Extract names from JSON-like data.
    Example:
    [{"id": 28, "name": "Action"}]

    becomes:

    ["Action"]
    """

    try:
        data = ast.literal_eval(text)

        return [item["name"] for item in data]

    except (ValueError, SyntaxError, TypeError):
        return []


# Genres
movies["genres"] = movies["genres"].apply(extract_names)

# Keywords
movies["keywords"] = movies["keywords"].apply(extract_names)


# --------------------------------------------------
# 5. EXTRACT TOP 3 CAST MEMBERS
# --------------------------------------------------

def extract_cast(text):
    try:
        data = ast.literal_eval(text)

        return [
            item["name"]
            for item in data[:3]
        ]

    except (ValueError, SyntaxError, TypeError):
        return []


movies["cast"] = movies["cast"].apply(extract_cast)


# --------------------------------------------------
# 6. EXTRACT DIRECTOR
# --------------------------------------------------

def extract_director(text):

    try:
        data = ast.literal_eval(text)

        for item in data:

            if item["job"] == "Director":
                return [item["name"]]

        return []

    except (ValueError, SyntaxError, TypeError):
        return []


movies["director"] = movies["crew"].apply(extract_director)

# We no longer need the full crew column
movies.drop(columns=["crew"], inplace=True)


# --------------------------------------------------
# 7. HANDLE MISSING VALUES
# --------------------------------------------------

movies["overview"] = movies["overview"].fillna("")

movies["runtime"] = movies["runtime"].fillna(
    movies["runtime"].median()
)

movies["release_date"] = movies["release_date"].fillna("")


# --------------------------------------------------
# 8. CREATE RELEASE YEAR
# --------------------------------------------------

movies["release_year"] = pd.to_datetime(
    movies["release_date"],
    errors="coerce"
).dt.year

movies["release_year"] = movies["release_year"].fillna(0).astype(int)


# --------------------------------------------------
# 9. CREATE A COMBINED TAG FIELD
# --------------------------------------------------

def create_tags(row):

    genres = " ".join(row["genres"])
    keywords = " ".join(row["keywords"])
    cast = " ".join(row["cast"])
    director = " ".join(row["director"])

    overview = row["overview"]

    return (
        genres + " "
        + keywords + " "
        + cast + " "
        + director + " "
        + overview
    )


movies["tags"] = movies.apply(create_tags, axis=1)


# --------------------------------------------------
# 10. CLEAN TAGS
# --------------------------------------------------

movies["tags"] = (
    movies["tags"]
    .str.lower()
    .str.replace(r"[^a-zA-Z0-9\s]", " ", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# --------------------------------------------------
# 11. KEEP FINAL FEATURES
# --------------------------------------------------

movies = movies[
    [
        "title",
        "genres",
        "keywords",
        "cast",
        "director",
        "overview",
        "vote_average",
        "vote_count",
        "runtime",
        "release_year",
        "popularity",
        "tags"
    ]
]


# --------------------------------------------------
# 12. SAVE CLEAN DATASET
# --------------------------------------------------

movies.to_csv(
    "dataset/processed_movies.csv",
    index=False
)


# --------------------------------------------------
# 13. DISPLAY RESULTS
# --------------------------------------------------

print("\n===================================")
print("DATA PREPARATION COMPLETED")
print("===================================")

print("\nFinal shape:")
print(movies.shape)

print("\nFinal columns:")
print(movies.columns.tolist())

print("\nFirst movie:")
print(movies.iloc[0])

print("\nMissing values:")
print(movies.isnull().sum())

print("\nSaved as:")
print("dataset/processed_movies.csv")