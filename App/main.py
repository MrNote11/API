from typing import Optional, Union

from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# API
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="FastApi_DataBase",
            user="postgres",
            password="DarkPunisher11",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("DataBase Connection Was Success")
        break
    except Exception as error:
        print("Connection Failed")
        print("Error: ", error)
        time.sleep(2)


# BaseModel Structure
class Post(BaseModel):
    title: str
    content: str
    publishing: bool = True
    rating: Optional[int] = 0


# fixing the id calling
# Create a def and give it a id argument for finding id.
def find_post(id):
    # incrementing the id in post
    for p in my_post:
        # passing id into post and cheacking it.
        if p["id"] == id:
            # returning p
            return p


# Enumerate the post
# create a def and make the argument id for enumerating.
def find_index_post(id):
    # enumrate for i to p
    for i, p in enumerate(my_post):
        # pass the id into p and check it
        if p["id"] == id:
            # return i
            return i


# the post Structure in list and dict format
my_post = [
    {"title": "title of post_1", "content": "content of post_1", "id": 1},
    {"title": "favorite_food", "content": "Pizza", "id": 2},
]


###################################################
# decorator
# Method
# Path
@app.get("/")
# Function
def read_root():
    return {"Hello": "World 100"}


# getting the post and giving it a path name
@app.get("/posts")
# def for the post
def get_posts():

    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    # return it in a dict format
    return {"data": posts}


##################################################################
# Creating a post and give it a status_code of created.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# But first create a body in the postman app.


# create a def function and initialized the argument into
# the BaseModel structure class
def create_post(post: Post):

    # Execute Sql the command u created and insert into the data
    # base you want and the values for each columns and returning
    # all the post object value to the schema,
    cursor.execute(
        """INSERT INTO posts(title, content, publishing, rating) VALUES(%s, %s, %s, %s) RETURNING *""",
        (post.title, post.content, post.publishing, post.rating),
    )

    new_Post = cursor.fetchone()

    conn.commit()
    return {"data": new_Post}


################################################################
# getting the latests post
@app.get("/posts/latest")
# Create a def
def get_latest_post():
    # create a variable that checks the the first index of
    # the post
    post = my_post[len(my_post) - 1]
    # create a return dict to see the results.
    return {"details": post}


################################################################
# get the lateset post and id
@app.get("/posts/{id}")

# create a def and argument that initilized the id is int
# and response as Resposnse to find the id of a post
def get_post(id: str, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    posts = cursor.fetchone()
    conn.commit()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This id of {id} doesnt exist")
    print(posts)
    # to check if a post id is not valid
    # create a raise exception of HTTPException
    return {"post details": posts}


#################################################################
# delete the post and give the arguments of the path and
# id with the status code of no content found.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)

# Create a def and arguments of the id that initilize int.
def delete(id: int):

    # use the enumerating function you created and pass the
    # id argument while creating a Variable to contain it.
    cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING *""", 
                   str((id)),)
    index_delete = cursor.fetchone()
    conn.commit()
    print(index_delete)
    # Create if the id you deleted or havent created is
    # still valid.
    if index_delete is None:

        # Create a raise Exception with the argument of
        # status_code and valuE status of 404
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail=f"post with id: {id} is null"
        )

    # use the my_post variable and use the pop function to
    # to make it a methid and pass the container you created
    # for the enumerate function.
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content=%s, publishing=%s WHERE id= %s
                   RETURNING *""",
                   (post.title, post.content, post.publishing, str(id)))
    index = cursor.fetchone()
    conn.commit()

    # Create if the id you deleted or havent created is
    # still valid.
    if index is None:

        # Create a raise Exception with the argument of
        # status_code and valuE status of 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} is null"
        )

    # use the my_post variable and use the pop function to
    # to make it a methid and pass the container you created
    # for the enumerate function.

    else:
        return {"data": index}
