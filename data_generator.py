"""Генератор даних: Онлайн-кінотеатр (варіант 14).
Виміри: directors, movies, subscribers. Факти: views, ratings.
Навмисні "брудні" дані: 10% NULL email, 5% дублікатів підписників,
20% NULL comment у ratings.
"""
import os
import random

import pandas as pd
from faker import Faker

fake = Faker("uk_UA")
Faker.seed(42)
random.seed(42)

os.makedirs("data_lake", exist_ok=True)

GENRES = ["Драма", "Комедія", "Бойовик", "Трилер", "Фантастика", "Жахи", "Мелодрама"]
DEVICES = ["TV", "Phone", "Laptop", "Tablet"]
PLANS = ["Basic", "Standard", "Premium"]


def generate_directors(n=30):
    return pd.DataFrame([{
        "director_id": i,
        "full_name": fake.name(),
        "country": fake.country(),
        "birth_year": random.randint(1940, 1995),
    } for i in range(1, n + 1)])


def generate_movies(director_ids, n=200):
    return pd.DataFrame([{
        "movie_id": i,
        "director_id": random.choice(director_ids),
        "title": fake.catch_phrase(),
        "genre": random.choice(GENRES),
        "release_year": random.randint(1990, 2025),
        "duration_min": random.randint(75, 180),
    } for i in range(1, n + 1)])


def generate_subscribers(n=1000):
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "subscriber_id": i,
            "full_name": fake.name(),
            "email": fake.email() if random.random() > 0.1 else None,  # 10% NULL
            "city": fake.city(),
            "plan": random.choice(PLANS),
            "registration_date": fake.date_between(start_date="-2y", end_date="today"),
        })
    df = pd.DataFrame(rows)
    duplicates = df.sample(frac=0.05, random_state=42)  # 5% дублікатів
    return pd.concat([df, duplicates], ignore_index=True)


def generate_views(subscriber_ids, movie_ids, n=10000):
    return pd.DataFrame([{
        "view_id": i,
        "subscriber_id": random.choice(subscriber_ids),
        "movie_id": random.choice(movie_ids),
        "view_date": fake.date_time_between(start_date="-1y", end_date="now"),
        "watch_duration_min": random.randint(1, 180),
        "device": random.choice(DEVICES),
    } for i in range(1, n + 1)])


def generate_ratings(subscriber_ids, movie_ids, n=3000):
    return pd.DataFrame([{
        "rating_id": i,
        "subscriber_id": random.choice(subscriber_ids),
        "movie_id": random.choice(movie_ids),
        "rating": random.randint(1, 5),
        "rating_date": fake.date_time_between(start_date="-1y", end_date="now"),
        "comment": fake.sentence(nb_words=10) if random.random() > 0.2 else None,  # 20% NULL
    } for i in range(1, n + 1)])


if __name__ == "__main__":
    print("Починаємо генерацію даних...")
    df_directors = generate_directors()
    df_movies = generate_movies(df_directors["director_id"].tolist())
    df_subscribers = generate_subscribers()

    # у фактах беремо унікальні ID (у subscribers є дублікати)
    sub_ids = df_subscribers["subscriber_id"].unique().tolist()
    movie_ids = df_movies["movie_id"].tolist()

    df_views = generate_views(sub_ids, movie_ids)
    df_ratings = generate_ratings(sub_ids, movie_ids)

    tables = {
        "directors": df_directors, "movies": df_movies,
        "subscribers": df_subscribers, "views": df_views, "ratings": df_ratings,
    }
    for name, df in tables.items():
        df.to_parquet(f"data_lake/raw_{name}.parquet", index=False)
        print(f"{name}: {len(df)} рядків")
    print("Готово! Файли у data_lake/")
