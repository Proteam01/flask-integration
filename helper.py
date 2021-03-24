"""
helper functions
"""
import yaml
from flask_sqlalchemy import SQLAlchemy


def read_database_options():
    """
    read database options
    """
    file = open('database.yml', 'r')
    data = file.read()
    file.close()
    load = yaml.load(data, Loader=yaml.FullLoader)
    return load


db = SQLAlchemy()
