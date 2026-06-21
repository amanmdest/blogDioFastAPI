from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.database import database
from src.controllers import auth, post
from src.exceptions import NotFoundPostError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield 
    await database.disconnect()


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Authentication operations.',
    },
    {
        'name': 'posts',
        'description': 'Manage blog posts.',
        'externalDocs': {
            'description': 'Posts.api external documentation.',
            'url': 'https://Posts.api.tiangolo.com/',
        },
    },
]

servers=[
    {'url': 'http://127.0.0.1:8000/', 'description': 'Staging environment'},
	{'url': 'https://blogdiofastapi.onrender.com/', 'description': 'Production environment'},
]

app = FastAPI(
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    servers=servers, 
    summary="Dio's favorite blog. Pucci said.",
    version='1.0.0',
    title='Dio blog API'
)
app.include_router(post.router, tags=['posts'])
app.include_router(auth.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
        )