from fastapi import FastAPI
from routes import chat

app = FastAPI()  # 👈 ОБЯЗАТЕЛЬНО НА ВЕРХУ

app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)