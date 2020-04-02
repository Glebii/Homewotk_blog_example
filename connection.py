import psycopg2 as pg


connection = pg.connect("user=postgres dbname=blog_example password=12345 host=localhost port=5555")
