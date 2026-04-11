from fastapi import FastAPI, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session

from models import Base, User, Post
from database import engine, session_local
from schemas import User as DbUser, UserCreate, PostCreate, PostResponse


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_user)

    return db_post


@app.get("/posts/", response_model=List[PostResponse])
async def posts(db: Session = Depends(get_db)) -> List[type[Post]]:
    return db.query(Post).all()


# @app.get("/")
# async def home() -> dict[str, str]:
#     return {"data": "message"}
#
#
# @app.get("/contacts")
# async def contacts() -> int:
#     return 42
#
#
# @app.get("/items")
# async def get_all_items() -> List[Post]:
#     return [Post(**post) for post in posts]
#
#
# @app.post("/items/add")
# async def add_item(post: PostCreate) -> Post:
#     author = next((user for user in users if user["id"] == post.author_id), None)
#     if not author:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#
#     new_post_id = len(posts) + 1
#
#     new_post = {
#         "id": new_post_id,
#         "title": post.title,
#         "body": post.body,
#         "author": author,
#     }
#     posts.append(new_post)
#     return Post(**new_post)
#
#
# # Модели валидируются через Body
# @app.post("/user/add")
# async def add_user(
#     user: Annotated[
#         UserCreate,
#         Body(
#             ...,
#             example={
#                 "name": "John",
#                 "age": 34,
#             },
#         ),
#     ],
# ) -> User:
#     new_user_id = len(users) + 1
#
#     new_user = {
#         "id": new_user_id,
#         "name": user.name,
#         "age": user.age,
#     }
#     posts.append(new_user)
#     return User(**new_user)
#
#
# # Path работает с динамическими параметрами например {id}
# @app.get("/items/{id}")
# async def get_item_by_id(
#     post_id: Annotated[
#         int, Path(..., title="Здесь указывается id поста", ge=1, lt=100)
#     ],
# ) -> Post:
#     for post in posts:
#         if post["id"] == post_id:
#             return Post(**post)
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
#
#
# # Query работает параметрами из get запроса, например ?post_id=1&...
# @app.get("/search")
# async def search(
#     post_id: Annotated[
#         Optional[int], Query(title="ID of post to search for", ge=1, le=50)
#     ],
# ) -> Dict[str, Optional[Post]]:
#     if post_id:
#         for post in posts:
#             if post["id"] == post_id:
#                 return {"data": Post(**post)}
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
#         )
#     else:
#         return {"data": None}
