import datetime

from typing import Annotated

from fastapi import APIRouter, Cookie, Header, Response, status
from schemas.post import PostIn
from views.post import PostOut

dt = datetime.datetime
router = APIRouter(prefix='/posts')
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


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(post: PostIn, response: Response):
    response.set_cookie(key='user', value='user@gmail.com', httponly=True)
    fake_db.append(post.model_dump())
    return post


@router.get('/', response_model=list[PostOut])
def read_posts(
    published: bool = True,
    ads_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    limit: int = 5,
    skip: int = 0, 
    ):
    print(f'Cookies: {ads_id}')
    print(f'User Agent: {user_agent}')
    return [post for post in fake_db[skip : skip + limit] if post['published'] is published]


@router.get('/{framework}', response_model=PostOut)
def read_framework_post(framework: str):
    return {
        "posts": [{
            'title': f'Criando uma aplicação com {framework}', 
            'date': dt.now(datetime.timezone.utc)},
            {'title': f'Internacionalizando uma app {framework}', 
            'date': dt.now()},
        ]}
