from typing import List
from collections import Counter
import re



# Функция для генерации истории
def generate_history(original_command: str, optimized_command: str, before_position: str, after_position: str) -> dict:
    from datetime import datetime
    return {
        "original_command": original_command,
        "optimized_command": optimized_command,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "before_position": before_position,
        "after_position": after_position
    }
