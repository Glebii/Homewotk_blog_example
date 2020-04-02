from flask import render_template, url_for, redirect, request , abort, current_app
from services import PostsService, CategoriesService, AuthorsService , UsersService , SessionsService


def index_page():
    """
    Функция обработчик запросов, получающая запрос и возвращающая html ответ из шаблона (index.html)

    Для формирования страницы используется сервис PostsService
    """
    posts = PostsService.get_all_posts()
    categories = CategoriesService.get_all_categories()
    authors = AuthorsService.get_all_authors()
    first_posts = posts[:2]
    posts = posts[2:]
    return render_template(
        "index.html",
        first_posts=first_posts,
        posts=posts,
        categories=categories,
        authors=authors,
    )


def post_page(post_id):
    post = PostsService.get_post_by_id(post_id)
    return render_template("article.html", post=post)


def category_page(category_id):
    category = CategoriesService.get_category_by_id(category_id)
    category_posts = PostsService.get_all_posts_by_category(category_id)
    return render_template(
        "category.html", category=category, category_posts=category_posts
    )


def author_page(author_id):
    author = AuthorsService.get_author_by_id(author_id)
    author_posts = PostsService.get_all_posts_by_author(author_id)
    return render_template("author.html", author=author, author_posts=author_posts)

# ADMIN ------------------------------------------------------------------------------------------------------
# Для ПОСТОВ ------------------------------------------------------------------------------------------------:
def admin_posts():
    posts = PostsService.get_all_posts()
    return render_template("admin_posts.html", posts=posts)


def admin_post_new():
    categories = CategoriesService.get_all_categories()
    authors = AuthorsService.get_all_authors()
    if request.method == "GET":
        return render_template(
            "admin_post.html", categories=categories, authors=authors
        )
    elif request.method == "POST":
        created_post = PostsService.create_new_post(
            request.form.get("title"),
            request.form.get("category_id"),
            request.form.get("author_id"),
            request.form.get("body"),
        )
        return redirect(url_for("admin_posts"))
def admin_post_edit(post_id: int):
    categories = CategoriesService.get_all_categories()
    authors = AuthorsService.get_all_authors()
    post = PostsService.get_post_by_id(post_id)
    if request.method == "GET":
        # Отрендерить шаблон admin_post.html для редактирования существующего поста
        return render_template(
            "admin_post_edit.html", categories=categories, authors=authors, post=post
        )
    elif request.method == "POST":
        # Редактируем существующий пост
        edited_post = PostsService.edit_post_by_id(
            post_id,
            request.form.get("title"),
            request.form.get("category_id"),
            request.form.get("author_id"),
            request.form.get("body"),
        )
        return redirect(url_for("admin_posts"))
def admin_posts_delete(post_id: int):
    PostsService.delete_pots_by_id(post_id)
    return redirect(url_for("admin_posts"))

#Для Категорий ----------------------------------------------------------------------------------------------:
def admin_categories():
    categories = CategoriesService.get_all_categories()
    return render_template("admin_categories.html", categories=categories)
def admin_category_delete(category_id: int):
    CategoriesService.delete_cat_by_id(category_id)
    return redirect(url_for("admin_categories"))
def admin_create_new_category():
    if request.method == "GET":
        return render_template("admin_create_category.html")
    elif request.method == "POST":
        created_category = CategoriesService.create_new_cat(
            request.form.get("title"),
        )
        return redirect(url_for("admin_categories"))
def admin_category_edit(category_id: int):
    category = CategoriesService.get_category_by_id(category_id)
    
    if request.method == "GET":
        # Отрендерить шаблон admin_post.html для редактирования существующего поста
        return render_template(
            "admin_category_edit.html", category=category
        )
    elif request.method == "POST":
        # Редактируем существующий пост
        edited_category = CategoriesService.edit_category_by_id(
            category_id,
            request.form.get("title")
        )
        return redirect(url_for("admin_categories"))





# Для Авторов -------------------------------------------------------------------------------------------------:
def admin_authors():
    authors = AuthorsService.get_all_authors()
    return render_template("admin_authors.html", authors=authors)
def admin_author_delete(author_id:int):
    AuthorsService.delete_author_by_id(author_id)
    return redirect(url_for("admin_authors"))
def admin_create_new_author():
    if request.method == "GET":
        return render_template("admin_create_author.html")
    elif request.method == "POST":
        created_author = AuthorsService.create_new_author(
            request.form.get("first_name"),
            request.form.get("last_name"),
        )
        return redirect(url_for("admin_authors"))
def admin_author_edit(author_id: int):
    author = AuthorsService.get_author_by_id(author_id)
    
    if request.method == "GET":
        # Отрендерить шаблон admin_post.html для редактирования существующего поста
        return render_template(
            "admin_author_edit.html", author=author
        )
    elif request.method == "POST":
        # Редактируем существующий пост
        edited_author = AuthorsService.edit_author_by_id(
            author_id,
            request.form.get("first_name"),
            request.form.get("last_name"),
        )
        return redirect(url_for("admin_authors"))

#User

def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = UsersService.get_user_by_username(username)
        if user.password != password:
            abort(400)
        st = request.cookies.get(current_app.config.get("SESSION_COOKIE"))
        SessionsService.attach_user(st, user.id)
        return redirect(url_for("index_page"))
#Регистрация роутов--------------------------------------------------------------------------------------------:
def register_views(app):
    app.route("/")(index_page)
    app.route("/post/<int:post_id>")(post_page)
    app.route("/category/<int:category_id>")(category_page)
    app.route("/author/<int:author_id>")(author_page)
    # ADMIN ----- Посты 
    app.route("/admin/")(admin_posts)  # Posts list
    app.route("/admin/post/<int:post_id>", methods=["DELETE"])(
        admin_posts_delete
    )  
    app.route("/admin/post/new", methods=["GET", "POST"])(admin_post_new)  # New post
    app.route("/admin/edit/post/<int:post_id>", methods=["GET", "POST"])(
        admin_post_edit
    )
    # ADMIN ------ Категории
    app.route("/admin/all categories/")(admin_categories)
    app.route("/admin/category/<int:category_id>", methods=["DELETE"])(
        admin_category_delete
    )
    app.route("/admin/category/new", methods=["GET", "POST"])(admin_create_new_category)
    app.route("/admin/edit/category/<int:category_id>", methods=["GET", "POST"])(
        admin_category_edit
    )
    # ADMIN ------ Авторы 
    app.route("/admin/all authors/")(admin_authors)
    app.route("/admin/author/<int:author_id>" ,methods=["DELETE"])(
        admin_author_delete
    )
    app.route("/admin/author/new", methods=["GET", "POST"])(admin_create_new_author)
    app.route("/admin/edit/author/<int:author_id>", methods=["GET", "POST"])(
        app.route("/admin/edit/author/<int:author_id>", methods=["GET", "POST"])(
        admin_author_edit
    )
    )
    #user
    app.route("/login", methods=["GET", "POST"])(login)