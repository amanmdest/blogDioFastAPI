import os

import databases
import sqlalchemy as sa

from src.config import settings


DATABASE_URL = settings.database_url

metadata = sa.MetaData()
database = databases.Database(DATABASE_URL)

if settings.environment == 'production':
    engine = sa.create_engine(DATABASE_URL)
else:
    engine = sa.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )