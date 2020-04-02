from typing import List
from dataclasses import dataclass
from connection import connection
from datetime import datetime


@dataclass
class AuthorDto:
    id: int
    first_name: str
    last_name: str

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class AuthorsService:
    @staticmethod
    def get_all_authors() -> List[AuthorDto]:
        c = connection.cursor()
        c.execute("SELECT id, first_name, last_name FROM authors;")
        data = c.fetchall()
        data = list(map(lambda i: AuthorDto(*i), data))
        return data

    @staticmethod
    def get_author_by_id(author_id: int) -> AuthorDto:
        c = connection.cursor()
        c.execute(
            "SELECT id, first_name, last_name FROM authors WHERE id=%s;", (author_id,)
        )
        data = c.fetchone()
        return AuthorDto(*data)
        
    @staticmethod
    def delete_author_by_id(author_id: int) -> AuthorDto:
       
        c = connection.cursor()
        author = AuthorsService.get_author_by_id(author_id)
        c.execute("DELETE FROM authors WHERE id=%s;", (author_id,))
        connection.commit()
        return author
    @staticmethod
    def create_new_author(first_name,last_name) -> AuthorDto:
        
        c = connection.cursor()
        c.execute(
            """INSERT INTO authors (first_name,last_name)
            VALUES (%s,%s) RETURNING id;""",
            (first_name,last_name),
        )
        author_id, = c.fetchone()
        connection.commit()
        author = AuthorsService.get_author_by_id(author_id)
        return author  
    @staticmethod
    def edit_author_by_id(author_id,first_name,last_name ) -> AuthorDto:
        
        c = connection.cursor()
        
        c.execute(
            """UPDATE authors SET first_name=%s,last_name=%s WHERE id=%s;""",
            (first_name,last_name, author_id)
        )
        connection.commit()
        author = AuthorsService.get_author_by_id(author_id)
        return author


