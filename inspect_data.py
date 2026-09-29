import pandas as pd

movies = pd.read_csv("dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb_5000_credits.csv")

print("MOVIES DATASET")
print("----------------")
print("Shape:", movies.shape)
print("Columns:")
print(movies.columns.tolist())

print("\nFirst 5 movies:")
print(movies.head())

print("\nCREDITS DATASET")
print("----------------")
print("Shape:", credits.shape)
print("Columns:")
print(credits.columns.tolist())

print("\nFirst 5 credits:")
print(credits.head())