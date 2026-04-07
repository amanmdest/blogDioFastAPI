import datetime

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
dt = datetime.datetime

fake_db = [
    {
        'title': f'Criando uma aplicação com Django', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
    {
        'title': f'Criando uma aplicação com FastAPI', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
    {
        'title': f'Criando uma aplicação com Flask', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
    {
        'title': f'Criando uma aplicação com Falcon', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
    {
        'title': f'Criando uma aplicação com Tornado', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
    {
        'title': f'Criando uma aplicação com Pyramid', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
    {
        'title': f'Criando uma aplicação com CherryPy', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
    {
        'title': f'Criando uma aplicação com Cottle', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
    {
        'title': f'Criando uma aplicação com Aiohttp', 
        'date': dt.now(datetime.timezone.utc),
        'published': True,
    },
]


class Post(BaseModel):
    title: str
    date: dt | None = None
    published: bool


@app.post('/posts/')
def create_post(post: Post):
    pass


@app.get('/posts/')
async def read_post(skip: int = 0, limit: int = len(fake_db), published: bool = True):
    return [post for post in fake_db[skip : skip + limit] if post['published'] is published]


@app.get('/posts/{framework}')
async def read_post_by_framework(framework: str):
    return {
        "posts": [{
            'title': f'Criando uma aplicação com {framework}', 
            'date': dt.now(datetime.timezone.utc)},
            {'title': f'Internacionalizando uma app {framework}', 
            'date': dt.now()},
        ]}
