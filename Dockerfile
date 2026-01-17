# Dockerfile
FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    sqlite3 \ 
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .




# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Добавить данные в БД
RUN python manage.py migrate
RUN python manage.py loaddata --exclude=contenttypes data.json



# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "map.wsgi:application"]
