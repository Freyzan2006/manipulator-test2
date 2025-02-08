from fastapi import FastAPI


import config.cors as config

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,  
    allow_credentials=config.ALLOW_CREDENTIALS,
    allow_methods=config.ALLOW_METHODS,  
    allow_headers=config.ALLOW_HEADERS,  
)



from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime
from typing import List
import re
import random

from .models import User
from .schemas import CommandRequest, CommandResponse, CommandHistory
from .services import generate_history




# Секретный ключ для JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# Модели для пользователей и паролей
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "$2b$12$DME0XzhmO03cF38h.nOZGQTjKpaDeKNtWcFmHNKpFiwPpQvZ1lGOa"  # "admin" зашифрованный
    }
}

# Парольный контекст
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 схема для авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Вспомогательные функции для хеширования пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    return None


# Авторизация через токен
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return {"access_token": form_data.username, "token_type": "bearer"}

history_list = []

# Команда на манипулятор
@app.post("/add_history")
async def add_history(command_request: CommandRequest):
    command = command_request.command
    optimize_command = command_request.optimizeCommand
    before_position = command_request.before
    after_position = command_request.after

    

    history_item = CommandHistory(
        command=command,
        optimize_command = optimize_command,
        date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        before_position=before_position,
        after_position=after_position
    )

    history_list.append(history_item)


    return {"command": f"{history_item}"}








# История всех команд
@app.get("/history", response_model=List[CommandHistory])
async def get_history():
    return history_list