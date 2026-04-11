from fastapi import FastAPI, HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User


class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int


users = [
    {"id": 1, "name": "John", "age": 34},
    {"id": 2, "name": "Alex", "age": 12},
    {"id": 3, "name": "Bob", "age": 45},
]


@app.get("/")
async def home() -> dict[str, str]:
    return {"data": "message"}


@app.get("/contacts")
async def contacts() -> int:
    return 42


posts = [
    {"id": 1, "title": "News 1", "body": "Text1", "author": users[1]},
    {"id": 2, "title": "News 2", "body": "Text2", "author": users[0]},
    {"id": 3, "title": "News 3", "body": "Text3", "author": users[2]},
]


@app.get("/items")
async def get_all_items() -> List[Post]:
    return [Post(**post) for post in posts]


@app.post("/items/add")
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user["id"] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")

    new_post_id = len(posts) + 1

    new_post = {
        "id": new_post_id,
        "title": post.title,
        "body": post.body,
        "author": author,
    }
    posts.append(new_post)
    return Post(**new_post)


@app.get("/items/{id}")
async def get_item_by_id(id: int) -> Post:
    for post in posts:
        if post["id"] == id:
            return Post(**post)
    raise HTTPException(status_code=404, detail="Post not found")


@app.get("/search")
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return {"data": Post(**post)}
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        return {"data": None}
