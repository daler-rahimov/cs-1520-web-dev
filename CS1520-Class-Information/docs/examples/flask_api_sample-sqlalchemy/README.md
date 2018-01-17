# flask_api_sample
simple example of using flask to generate an api

## Dependencies

`pip install -r requirements.txt`

* [Flask](http://flask.pocoo.org/)
* [Requests](http://docs.python-requests.org/en/latest/)
* [flask-httpauth](https://flask-httpauth.readthedocs.org/en/latest/)
* [passlib](https://pythonhosted.org/passlib/)
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)

## How to Use

From a command line run:

* `export FLASK_APP=flask_api.py`
* `flask initdb`
* `flask run` (Runs the service on `http://localhost:5000`) 

A list of `curl` commands to test the REST API is included in `curl_commands.txt`.

To test the api service using the Front End flask app, open another command line and run `python front_end.py` (Runs the app on `http://localhost:5001`).

This sample uses a simple list of objects as our data store. The principles can be easily transferred to using a backend of your choice.

On the browser go to `http://localhost:5001` to view the front end portion.

You can run tests from the command line by running `python api_tests.py`.

## Future Work

Also, it would be nice to set up a [Vagrant]('https://www.vagrantup.com/') script for launching a VM with all the dependencies pre-installed so users could see it working without installing and configuring dependencies themselves. Or [Docker](https://www.docker.com/) :).

## Acknowledgements

In preparing this demo, I consulted and pulled from a few tutorials online:

* [Designing a RESTful API with Python and Flask](http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)
* [RESTful Authentication with Flask](http://blog.miguelgrinberg.com/post/restful-authentication-with-flask)
* [How to Build an API with Python and Flask](http://tech.pro/tutorial/1213/how-to-build-an-api-with-python-and-flask)
* [PassLib Tutorials](https://pythonhosted.org/passlib/)
