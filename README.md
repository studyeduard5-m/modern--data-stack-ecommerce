# Modern Data Stack: Онлайн-кінотеатр

Цей проєкт створює сирий шар (Raw) сховища даних для онлайн-кінотеатру. Це лабораторна робота №1 з курсу «Технології сховищ даних».

## Архітектура

Python (Faker, Pandas) -> Docker PostgreSQL (схема `raw`)

## Таблиці

| Таблиця     | Тип   | Опис                      |
|-------------|-------|---------------------------|
| subscribers | Вимір | Підписники                |
| movies      | Вимір | Фільми                    |
| directors   | Вимір | Режисери                  |
| views       | Факт  | Перегляди                 |
| ratings     | Факт  | Оцінки та коментарі       |

## Дані з помилками

Скрипт створює дані з помилками. Помилки лишаються в шарі `raw`.

- У таблиці `subscribers` 10% значень `email` дорівнюють NULL.
- У таблиці `ratings` 20% значень `comment` дорівнюють NULL.



## Запуск проєкту

1. Склонуйте репозиторій.
2. Створіть віртуальне середовище:

   ```bash
   python -m venv venv
   ```

3. Активуйте віртуальне середовище:

   ```bash
   # Windows
   venv\Scripts\activate
   # Mac або Linux
   source venv/bin/activate
   ```

4. Встановіть бібліотеки:

   ```bash
   pip install -r requirements.txt
   ```

5. Запустіть контейнер PostgreSQL:

   ```bash
   docker compose up -d
   ```

6. Запустіть скрипт:

   ```bash
   python data_generator.py
   ```

Скрипт генерує дані та завантажує їх у схему `raw`.

## Параметри підключення

| Параметр     | Значення      |
|--------------|---------------|
| Хост         | localhost     |
| Порт         | 5432          |
| База даних   | cinema_dwh    |
| Користувач   | admin         |
| Пароль       | adminpassword |

## Перевірка

Виконайте ці запити в базі даних:

```sql
SELECT COUNT(*) FROM raw.views;
SELECT COUNT(*) FROM raw.subscribers WHERE email IS NULL;
SELECT COUNT(*) FROM raw.ratings WHERE comment IS NULL;
```

## Повторний запуск

Скрипт використовує `if_exists='replace'`. Ви можете безпечно запустити скрипт повторно. Скрипт замінює старі таблиці новими.

## Зупинка проєкту

Зупиніть контейнер:

```bash
docker compose down
```

Щоб видалити також дані, виконайте `docker compose down -v`.
