"""This module contains functions to connect to DB and to get info about defined tables and DB's revision slug."""

from typing import List

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from sql.config import *


sqlalchemy_url = db_url if db_url is not None \
    else f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

Base = declarative_base()

_engine = None
_Session = None
_session = None


def create_session() -> Session:
    """
    Initializing connection to DB, if not yet exist.
    Creates and returns the session object.

    Returns:
        Session: session object to performs operations in DB.
    """
    global _engine, _Session, _session
    if _engine is None:
        _engine = create_engine(sqlalchemy_url)
        Base.metadata.bind = _engine
        Base.metadata.create_all(_engine)
    if _Session is None:
        _Session = scoped_session(sessionmaker(bind=_engine))

    if _session is None:
        _session = _Session()
    return _session


def get_tables() -> List[str]:
    """
    Creating session if not exist.

    Returns:
        List[str]: list of table names existing in database.
    """
    create_session()

    from sqlalchemy import inspect
    inspector = inspect(_engine)

    tables = [table_name for table_name in inspector.get_table_names()]
    # for column in inspector.get_columns(table_name):
    #     print("Column: %s" % column['name'])
    return tables


def get_database_revision() -> str:
    """
    Creating session if not exist.

    :return: alembic revision slug
    """
    session = create_session()

    from sqlalchemy.schema import MetaData, Table
    meta = MetaData(bind=_engine, reflect=True)
    versions = Table('alembic_version', meta, autoload=True, autoload_with=_engine)

    version: str = session.query(versions).all()[-1][0]
    session.close()
    return version


__all__ = [
    'create_session',
    'get_tables',
    'get_database_revision'
]

# def update_last_index(db: MySQLConnection, table_name: str, column_name: str):
#     """
#     Set the index of auto-increment column to the last used
#     :param db:
#     :param table_name: the name of the table to update the index in
#     :param column_name: the name of the column to set the index for
#     """
#     cursor = db.cursor()
#     s = "SELECT MAX(%s) FROM %s" % (column_name, table_name)
#     cursor.execute(s)
#     last_id = cursor.fetchall()
#     # print(last_id, table_name)
#     last_id = last_id[0][0]
#     if last_id:
#         last_id = int(last_id)
#         cursor.execute("ALTER TABLE " + table_name + " auto_increment = %s", (last_id,))
#     else:
#         cursor.execute("ALTER TABLE " + table_name + " auto_increment = 0")
#     db.commit()
