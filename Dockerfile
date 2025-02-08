# Используем официальный Python образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Команда для запуска приложения с Gunicorn
CMD ["gunicorn", "app.main:app", "--workers", "3", "--bind", "0.0.0.0:8000"]