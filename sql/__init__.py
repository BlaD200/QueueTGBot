from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from sql.config import *


sqlalchemy_url = db_url if db_url is not None \
    else f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

_engine = None
_Session = None


def create_session() -> Session:
    global _engine, _Session
    if _engine is None:
        _engine = create_engine(sqlalchemy_url)
    if _Session is None:
        _Session = sessionmaker(bind=_engine)

    session: Session = _Session()
    return session


def get_tables() -> List[str]:
    from sqlalchemy import inspect
    inspector = inspect(_engine)

    tables = [table_name for table_name in inspector.get_table_names()]
    # for column in inspector.get_columns(table_name):
    #     print("Column: %s" % column['name'])
    return tables


def get_database_revision() -> str:
    from sqlalchemy.schema import MetaData, Table
    meta = MetaData(bind=_engine, reflect=True)
    versions = Table('alembic_version', meta, autoload=True, autoload_with=_engine)

    session = create_session()
    version: str = session.query(versions).all()[-1][0]
    session.close()
    return version

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
