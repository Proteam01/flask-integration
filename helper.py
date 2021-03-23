import yaml
from flask_sqlalchemy import SQLAlchemy


def read_database_options():
    f = open('database.yml', 'r')
    data = f.read()
    f.close()
    load = yaml.load(data,Loader=yaml.FullLoader)
    return load


db = SQLAlchemy()

