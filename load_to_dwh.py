"""Завантаження parquet-файлів з data_lake у схему raw PostgreSQL (Full Load)."""
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = "postgresql://admin:adminpassword@localhost:5432/cinema_dwh"
engine = create_engine(DB_URL)

TABLES = ["directors", "movies", "subscribers", "views", "ratings"]


def load_data_to_dwh():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()

    for name in TABLES:
        print(f"Завантаження {name}...")
        df = pd.read_parquet(f"data_lake/raw_{name}.parquet")
        # replace = ідемпотентний повний перезапис: повторний запуск безпечний
        df.to_sql(name, engine, schema="raw", if_exists="replace", index=False)

    print("Дані успішно завантажені у схему 'raw'!")


if __name__ == "__main__":
    load_data_to_dwh()
