from typing import List
from dataclasses import dataclass
from connection import connection



@dataclass
class CategoryDto:
    id: int
    title: str


class CategoriesService:
    @staticmethod
    def get_all_categories() -> List[CategoryDto]:
        c = connection.cursor()
        c.execute("SELECT id, title FROM categories;")
        data = c.fetchall()
        data = list(map(lambda i: CategoryDto(*i), data))
        return data

    @staticmethod
    def get_category_by_id(category_id: int) -> CategoryDto:
        c = connection.cursor()
        c.execute("SELECT id, title FROM categories WHERE id=%s;", (category_id,))
        data = c.fetchone()
        return CategoryDto(*data)
    @staticmethod
    def delete_cat_by_id(category_id: int) -> CategoryDto:
       
        c = connection.cursor()
        category = CategoriesService.get_category_by_id(category_id)
        c.execute("DELETE FROM categories WHERE id=%s;", (category_id,))
        connection.commit()
        return category
    @staticmethod
    def create_new_cat(title) -> CategoryDto:
        
        c = connection.cursor()
        c.execute(
            """INSERT INTO categories (title)
            VALUES (%s) RETURNING id;""",
            (title,),
        )
        category_id, = c.fetchone()
        connection.commit()
        category = CategoriesService.get_category_by_id(category_id)
        return category   
    @staticmethod
    def edit_category_by_id(category_id, title) -> CategoryDto:
        
        c = connection.cursor()
        
        c.execute(
            """UPDATE categories SET title=%s WHERE id=%s;""",
            (title , category_id)
        )
        connection.commit()
        category = CategoriesService.get_category_by_id(category_id)
        return category
