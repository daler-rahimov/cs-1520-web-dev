#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from passlib.apps import custom_app_context as pwd_context
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

db = SQLAlchemy()


def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    year = db.Column(db.Integer)
    rating = db.Column(db.String(5))
    released = db.Column(db.String(20))
    runtime = db.Column(db.String(15))
    genre = db.Column(db.Text(length=None))
    director = db.Column(db.String(256))
    writer = db.Column(db.String(256))
    actors = db.Column(db.String(512))
    plot = db.Column(db.Text(length=None))
    language = db.Column(db.String(100))
    country = db.Column(db.String(100))
    awards = db.Column(db.String(512))
    poster = db.Column(db.String(512))
    metascore = db.Column(db.String(5))
    imdbRating = db.Column(db.Float())
    
    def __repr__(self):
        return "<Movie {}>".format(repr(self.title))

    @property
    def json(self):
        return to_json(self, self.__class__)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(512))

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def json(self):
        return {'user': self.username, 'id': self.id}
