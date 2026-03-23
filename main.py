from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def home() -> dict[str, str]:
    return {"data": "message"}

@app.get("/contacts")
async def contacts() -> int:
    return 42

posts = [
    {'id': 1, 'title': 'News 1', 'body': 'Text1 '},
    {'id': 2, 'title': 'News 2', 'body': 'Text2 '},
    {'id': 3, 'title': 'News 3', 'body': 'Text3 '},
]

@app.get("/items")
async def items() -> list:
    return posts

@app.get("/items/{id}")
async def items(id: int) -> dict:
    for post in posts:
        if post['id'] == id:
            return post
    raise HTTPException(status_code=404, detail='Post not found')


