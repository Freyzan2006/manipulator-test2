from pydantic import BaseModel
from typing import List, Optional


class CommandRequest(BaseModel):
    command: str
    optimizeCommand: str 
    before: str 
    after: str 


class CommandResponse(BaseModel):
    command: str
    


class CommandHistory(BaseModel):
    command: str
    optimize_command: str 
    date_time: str
    before_position: str
    after_position: str