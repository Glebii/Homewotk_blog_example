from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from connection import connection


@dataclass
class UserDto:
    id: int
    username: str
    password: str
    created_at: datetime
    updated_at: datetime


class UsersService:
    @staticmethod
    def get_user_by_username(username: str) -> UserDto:
        c = connection.cursor()
        c.execute(
            "SELECT id, username, password, created_at, updated_at from users WHERE username=%s;",
            (username,),
        )
        user_data = c.fetchone()
        return UserDto(*user_data)