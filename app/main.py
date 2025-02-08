

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import re
import random

from .models import User
from .schemas import CommandRequest, CommandResponse, CommandHistory
from .services import generate_history

import config.cors as config

app = FastAPI()
history_list = []


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,  
    allow_credentials=config.ALLOW_CREDENTIALS,
    allow_methods=config.ALLOW_METHODS,  
    allow_headers=config.ALLOW_HEADERS,  
)






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


@app.get("/history", response_model=List[CommandHistory])
async def get_history():
    return history_list