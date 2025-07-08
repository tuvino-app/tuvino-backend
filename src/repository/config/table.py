import typing

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase


class DBTable(DeclarativeBase):
    metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()  # type: ignore


Base: typing.Type[DeclarativeBase] = DBTable

from src.repository.table_models import *