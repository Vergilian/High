FROM python:3.11

#Рабочая директория
WORKDIR /app

#Зависимости и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
