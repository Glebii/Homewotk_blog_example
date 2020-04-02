from typing import List
from dataclasses import dataclass
from connection import connection
from datetime import datetime


@dataclass
class PostDto:
    id: int
    title: str
    body: str
    create_at: datetime
    updated_at: datetime
    author_id: int
    author_first_name: str
    author_last_name: str
    category_title: str


POST_DTO_SELECT_SQL = """
                posts.id,
                posts.title,
                body,
                create_at,
                updated_at,
                author_id,
                authors.first_name AS author_first_name,
                authors.last_name AS author_last_name,
                categories.title AS category_title"""

POST_DTO_FROM_SQL = """
                posts
                LEFT JOIN authors ON posts.author_id = authors.id
                LEFT JOIN categories ON posts.category_id= categories.id"""


class PostsService:
    @staticmethod
    def get_all_posts() -> List[PostDto]:
        c = connection.cursor()
        c.execute(
            f"""
            SELECT
                {POST_DTO_SELECT_SQL}
            FROM
                {POST_DTO_FROM_SQL}
            ORDER BY create_at DESC;
        """
        )
        data = c.fetchall()  # [(), ()]
        data = list(map(lambda i: PostDto(*i), data))
        return data

    @staticmethod
    def get_all_posts_by_category(category_id) -> List[PostDto]:
        c = connection.cursor()
        c.execute(
            f"""
            SELECT
                {POST_DTO_SELECT_SQL}
            FROM
                {POST_DTO_FROM_SQL}
            WHERE
                posts.category_id=%s
            ORDER BY created_at DESC;
        """,
            (category_id,),
        )
        data = c.fetchall()
        data = list(map(lambda i: PostDto(*i), data))
        return data

    @staticmethod
    def get_all_posts_by_author(author_id) -> List[PostDto]:
        c = connection.cursor()
        c.execute(
            f"""
            SELECT
                {POST_DTO_SELECT_SQL}
            FROM
                {POST_DTO_FROM_SQL}
            WHERE
                posts.author_id=%s
            ORDER BY create_at DESC;
        """,
            (author_id,),
        )
        data = c.fetchall()
        data = list(map(lambda i: PostDto(*i), data))
        return data

    @staticmethod
    def get_post_by_id(post_id: int) -> PostDto:
        c = connection.cursor()
        c.execute(
            f"""
            SELECT
                {POST_DTO_SELECT_SQL}
            FROM
                {POST_DTO_FROM_SQL}
            WHERE posts.id=%s;
        """,
            (post_id,),
        )
        data = c.fetchone()
        data = PostDto(*data)
        return data

    @staticmethod
    def create_new_post(title, category_id, author_id, body="") -> PostDto:
        """
        Создать новый пост с полученными данными и вернуть его
        """
        c = connection.cursor()
        now = datetime.now()
        c.execute(
            """INSERT INTO posts (title, category_id, author_id, body, create_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;""",
            (title, category_id, author_id, body, now, now),
        )
        post_id, = c.fetchone()
        connection.commit()
        post = PostsService.get_post_by_id(post_id)
        return post
    @staticmethod
    def edit_post_by_id(post_id, title, category_id, author_id, body="") -> PostDto:
        """
        Редактирует существующий пост по id и возвращает новую версию
        """
        c = connection.cursor()
        now = datetime.now()
        c.execute(
            """UPDATE posts SET title=%s, category_id=%s, author_id=%s, body=%s, updated_at=%s WHERE id=%s;""",
            (title, category_id, author_id, body, now, post_id)
        )
        connection.commit()
        post = PostsService.get_post_by_id(post_id)
        return post
    @staticmethod
    def delete_pots_by_id(post_id: int) -> PostDto:
        """
        Удалить пость по его ID и вернуть его после удаления.
        """
        c = connection.cursor()
        post = PostsService.get_post_by_id(post_id)
        c.execute("DELETE FROM posts WHERE id=%s;", (post.id,))
        connection.commit()
        return post
