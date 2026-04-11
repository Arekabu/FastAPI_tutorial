from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    age: int


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    model_config = {"json_schema_extra": {"examples": [{"name": "Jimmie", "age": 42}]}}


class PostBase(BaseModel):
    title: str
    body: str
    author_id: int


class PostCreate(PostBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "New post title", "body": "New post body", "author_id": 1}
            ]
        }
    }


class PostResponse(PostBase):
    id: int
    author: User

    class Config:
        from_attributes = True
