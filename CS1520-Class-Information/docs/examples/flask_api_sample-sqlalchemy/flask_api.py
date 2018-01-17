#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from flask import Flask, jsonify, abort, request, url_for
from models import db, User, Movie
from bootstrap_models import movies
from flask_restful import Api
from resources import (
    MovieResource, 
    MovieListResource, 
    UserResource, 
    UserListResource
)

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'flask_api.db')
))

api = Api(app, prefix="/api")
db.init_app(app)

api.add_resource(MovieListResource, '/movies/', endpoint='movies')
api.add_resource(MovieResource, '/movies/<int:id>', endpoint='movie')
api.add_resource(UserListResource, '/users/', endpoint='users' )
api.add_resource(UserResource, '/users/<string:username>', endpoint='user' )


#########################
# Flask CLI Commands    #
#########################

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.drop_all()
    db.create_all()

    admin = User(username='twaits', password_hash=User.hash_password('Passphrase1'))
    db.session.add(admin)
    db.session.commit()

    print('Adding Admin: %s' % admin.username)

    for movie in movies:
        print('Adding Movie: %s' % movie['title'])
        m = Movie(
                title=movie['title'],
                year=movie['year'],
                rating=movie['rating'],
                released=movie['released'],
                runtime=movie['runtime'],
                genre=movie['genre'],
                director=movie['director'],
                writer=movie['writer'],
                actors=movie['actors'],
                plot=movie['plot'],
                language=movie['language'],
                country=movie['country'],
                awards=movie['awards'],
                poster=movie['poster'],
                metascore=movie['metascore'],
                imdbRating=movie['imdbRating']
            )
        db.session.add(m)
        db.session.commit()

    print('Initialized the database.')


if __name__ == "__main__":
    app.run(debug=True)
