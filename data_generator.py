import pandas as pd
from faker import Faker
import random
from sqlalchemy import create_engine, text

fake = Faker()
Faker.seed(42)
random.seed(42)


def generate_directors(num=1000):
    directors = []
    for i in range(1, num + 1):
        directors.append({
            'director_id': i,
            'name': fake.name(),
            'country': fake.country(),
            'birth_year': random.randint(1940, 1995)
        })
    return pd.DataFrame(directors)


def generate_movies(directors_df, num=10000):
    movies = []
    director_ids = directors_df['director_id'].tolist()
    for i in range(1, num + 1):
        movies.append({
            'movie_id': i,
            'director_id': random.choice(director_ids),
            'title': fake.word().capitalize() + " " + fake.word(),
            'genre': random.choice(['Drama', 'Comedy', 'Action', 'Thriller', 'Sci-Fi']),
            'release_year': random.randint(1990, 2025),
            'duration_min': random.randint(75, 180)
        })
    return pd.DataFrame(movies)


def generate_subscribers(num=50000):
    subscribers = []
    for i in range(1, num + 1):
        email = fake.email() if random.random() > 0.1 else None  # 10% пропущених email
        subscribers.append({
            'subscriber_id': i,
            'name': fake.name(),
            'email': email,
            'plan': random.choice(['Basic', 'Standard', 'Premium']),
            'registration_date': fake.date_between(start_date='-2y', end_date='today')
        })
    return pd.DataFrame(subscribers)


def generate_views(subscribers_df, movies_df, num=500000):
    views = []
    subscriber_ids = subscribers_df['subscriber_id'].tolist()
    movie_ids = movies_df['movie_id'].tolist()
    for i in range(1, num + 1):
        views.append({
            'view_id': i,
            'subscriber_id': random.choice(subscriber_ids),
            'movie_id': random.choice(movie_ids),
            'watch_duration_min': random.randint(1, 180),
            'view_date': fake.date_time_between(start_date='-1y', end_date='now')
        })
    return pd.DataFrame(views)


def generate_ratings(subscribers_df, movies_df, num=150000):
    ratings = []
    subscriber_ids = subscribers_df['subscriber_id'].tolist()
    movie_ids = movies_df['movie_id'].tolist()
    for i in range(1, num + 1):
        comment = fake.sentence() if random.random() > 0.2 else None  # 20% пустих comment
        ratings.append({
            'rating_id': i,
            'movie_id': random.choice(movie_ids),
            'subscriber_id': random.choice(subscriber_ids),
            'rating': random.randint(1, 5),
            'comment': comment
        })
    return pd.DataFrame(ratings)


df_directors = generate_directors()
df_movies = generate_movies(df_directors)
df_subscribers = generate_subscribers()
df_views = generate_views(df_subscribers, df_movies)
df_ratings = generate_ratings(df_subscribers, df_movies)

print(f"Згенеровано: {len(df_directors)} directors, {len(df_movies)} movies, "
      f"{len(df_subscribers)} subscribers, {len(df_views)} views, {len(df_ratings)} ratings.")

DB_URL = "postgresql://admin:adminpassword@localhost:5432/cinema_dwh"
engine = create_engine(DB_URL)


def load_data_to_dwh():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()

    print("Завантаження directors...")
    df_directors.to_sql('directors', engine, schema='raw', if_exists='replace', index=False, chunksize=10000)

    print("Завантаження movies...")
    df_movies.to_sql('movies', engine, schema='raw', if_exists='replace', index=False, chunksize=10000)

    print("Завантаження subscribers...")
    df_subscribers.to_sql('subscribers', engine, schema='raw', if_exists='replace', index=False, chunksize=10000)

    print("Завантаження views...")
    df_views.to_sql('views', engine, schema='raw', if_exists='replace', index=False, chunksize=10000)

    print("Завантаження ratings...")
    df_ratings.to_sql('ratings', engine, schema='raw', if_exists='replace', index=False, chunksize=10000)

    print("Дані успішно завантажені у схему 'raw'!")


if __name__ == "__main__":
    load_data_to_dwh()