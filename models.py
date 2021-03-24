"""
models file
"""
# pylint: disable=E1101
# pylint: disable=R0903
from helper import db


class Book(db.Model):
    """
    models class database sqlalchemy
    """
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    type = db.Column(db.String(250))
    created = db.Column(db.Date())
