"""This module reads environment variables related to DB to python variables."""

from os import getenv


db_username = getenv('DATABASE_USERNAME')
db_password = getenv('DATABASE_PASSWORD')
db_host = getenv('DATABASE_HOST')
db_port = getenv('DATABASE_PORT')
db_name = getenv('DATABASE_NAME')

db_url = getenv('DATABASE_URL')
