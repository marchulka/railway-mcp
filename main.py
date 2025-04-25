main.py
python
Копировать
Редактировать
from fastapi import FastAPI
from routes import chat

app = FastAPI()

# Подключаем маршруты (в частности /next-task)
app.include_router(chat.router)

# Прямой запуск сервера при локальной работе (или в Railway через Docker)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)