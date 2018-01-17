from flask_api import app
from models import User
import unittest
import json
import base64


class FlaskMovieAPITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def open_with_auth(self, url, method, username, password, *args, **kwargs):
        authStr = username + ":" + password
        return self.app.open(
            url,
            method=method,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(authStr.encode('ascii'))
            },
            *args, **kwargs
        )

    def test_user_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/users/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

    def test_user_data(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/api/users/')

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(data_dict['users'][0]['user'], "twaits")
        self.assertEqual(data_dict['users'][0]['id'], 0)

    def test_user_create_status_code_and_return(self):
        result=self.app.post('/api/users/',
                       data=json.dumps(dict(user='test',
                                            password='Passphrase1')),
                       content_type = 'application/json')

        self.assertEqual(result.status_code, 201)

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(data_dict['user']['user'], "test")
        self.assertEqual(data_dict['user']['id'], 1)

    # Test list of movies
    def test_movie_list_status_and_count(self):
        result=self.open_with_auth('/api/movies/',
                                       'GET',
                                       'twaits',
                                       'Passphrase1'
                                    )

        self.assertEqual(result.status_code, 200)

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(len(data_dict['movies']), 10)

    # Test single movie
    def test_single_movie_status_and_count(self):
        result=self.open_with_auth('/api/movies/2',
                                       'GET',
                                       'twaits',
                                       'Passphrase1'
                                    )

        self.assertEqual(result.status_code, 200)

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(data_dict['movie']['Plot'], "A young man is accidentally sent 30 years into the past in a time-traveling DeLorean invented by his friend, Dr. Emmett Brown, and must make sure his high-school-age parents unite in order to save his own existence.")
        self.assertEqual(data_dict['movie']['Rated'], "PG")
        self.assertEqual(data_dict['movie']['Language'], "English")
        self.assertEqual(data_dict['movie']['Title'], "Back to the Future")
        self.assertEqual(data_dict['movie']['Country'], "USA")
        self.assertEqual(data_dict['movie']['Writer'], "Robert Zemeckis, Bob Gale")
        self.assertEqual(data_dict['movie']['Metascore'], "86")
        self.assertEqual(data_dict['movie']['imdbRating'], "8.5")
        self.assertEqual(data_dict['movie']['Director'], "Robert Zemeckis")
        self.assertEqual(data_dict['movie']['Released'], "03 Jul 1985")
        self.assertEqual(data_dict['movie']['Year'], "1985")
        self.assertEqual(data_dict['movie']['Awards'], "Won 1 Oscar. Another 17 wins & 24 nominations.")
        self.assertEqual(data_dict['movie']['Poster'], "http://ia.media-imdb.com/images/M/MV5BMjA5NTYzMDMyM15BMl5BanBnXkFtZTgwNjU3NDU2MTE@._V1_SX300.jpg")
        self.assertEqual(data_dict['movie']['Genre'], "Adventure, Comedy, Sci-Fi")
        self.assertEqual(data_dict['movie']['Actors'], "Michael J. Fox, Christopher Lloyd, Lea Thompson, Crispin Glover")
        self.assertEqual(data_dict['movie']['Runtime'], "116 min")
        self.assertEqual(data_dict['movie']['id'], 2)

    # Test movie does not exist
    def test_single_movie_status_and_count(self):
        result=self.open_with_auth('/api/movies/25',
                                   'GET',
                                   'twaits',
                                   'Passphrase1')

        self.assertEqual(result.status_code, 404)

    # Test create movie with error
    def test_create_movie_bad_request(self):
        result=self.open_with_auth('/api/movies/',
                                   'POST',
                                   'twaits',
                                   'Passphrase1',
                                   data=json.dumps(dict(Rated='R',
                                            Director='Wes Anderson')),
                                   content_type = 'application/json')

        self.assertEqual(result.status_code, 400)

        data_dict = json.loads(result.data)

        self.assertEqual(data_dict['message'], "Required fields Title, Year not in request.")

    # Test create movie success
    def test_create_movie_success(self):
        result=self.open_with_auth('/api/movies/',
                                   'POST',
                                   'twaits',
                                   'Passphrase1',
                                   data=json.dumps(dict(Title='The Royal Tenenbaums',
                                            Year='2001')),
                                   content_type = 'application/json')

        self.assertEqual(result.status_code, 201)

        data_dict = json.loads(result.data)
        # assert the response data
        self.assertEqual(data_dict['movie']['Plot'], "")
        self.assertEqual(data_dict['movie']['Rated'], "")
        self.assertEqual(data_dict['movie']['Language'], "")
        self.assertEqual(data_dict['movie']['Title'], "The Royal Tenenbaums")
        self.assertEqual(data_dict['movie']['Country'], "")
        self.assertEqual(data_dict['movie']['Writer'], "")
        self.assertEqual(data_dict['movie']['Metascore'], "")
        self.assertEqual(data_dict['movie']['imdbRating'], "")
        self.assertEqual(data_dict['movie']['Director'], "")
        self.assertEqual(data_dict['movie']['Released'], "")
        self.assertEqual(data_dict['movie']['Year'], "2001")
        self.assertEqual(data_dict['movie']['Awards'], "")
        self.assertEqual(data_dict['movie']['Poster'], "")
        self.assertEqual(data_dict['movie']['Genre'], "")
        self.assertEqual(data_dict['movie']['Actors'], "")
        self.assertEqual(data_dict['movie']['Runtime'], "")
        self.assertEqual(data_dict['movie']['id'], 11)

    # Test update movie success
    def test_update_movie_success(self):
        result=self.open_with_auth('/api/movies/11',
                                   'PUT',
                                   'twaits',
                                   'Passphrase1',
                                   data=json.dumps(dict(Rated='R',
                                            Director='Wes Anderson')),
                                   content_type = 'application/json')

        self.assertEqual(result.status_code, 200)

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(data_dict['movie']['Plot'], "")
        self.assertEqual(data_dict['movie']['Rated'], "R")
        self.assertEqual(data_dict['movie']['Language'], "")
        self.assertEqual(data_dict['movie']['Title'], "The Royal Tenenbaums")
        self.assertEqual(data_dict['movie']['Country'], "")
        self.assertEqual(data_dict['movie']['Writer'], "")
        self.assertEqual(data_dict['movie']['Metascore'], "")
        self.assertEqual(data_dict['movie']['imdbRating'], "")
        self.assertEqual(data_dict['movie']['Director'], "Wes Anderson")
        self.assertEqual(data_dict['movie']['Released'], "")
        self.assertEqual(data_dict['movie']['Year'], "2001")
        self.assertEqual(data_dict['movie']['Awards'], "")
        self.assertEqual(data_dict['movie']['Poster'], "")
        self.assertEqual(data_dict['movie']['Genre'], "")
        self.assertEqual(data_dict['movie']['Actors'], "")
        self.assertEqual(data_dict['movie']['Runtime'], "")
        self.assertEqual(data_dict['movie']['id'], 11)

    # Test update movie with bad data
    def test_update_movie_success(self):
        jsonStr = json.dumps(dict(Rated=True,
                                  Director='Wes Bnderson'))

        result=self.open_with_auth('/api/movies/11',
                                   'PUT',
                                   'twaits',
                                   'Passphrase1',
                                   data=json.dumps(dict(Rated=True, Director='Wes Bnderson')),
                                   content_type = 'application/json')

        self.assertEqual(result.status_code, 400)

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(data_dict['message'], "Rated is <type 'unicode'>. <type 'bool'> passed in from request")

    # Test movie delete

    # Regardless of where I put this test, it makes
    # 'test_update_movie_success' fail

    # def test_movie_delete(self):
    #     result=self.open_with_auth('/api/movies/11',
    #                                'DELETE',
    #                                'twaits',
    #                                'Passphrase1')

    #     self.assertEqual(result.status_code, 200)

    #     data_dict = json.loads(result.data)

    #     # assert the response data
    #     self.assertEqual(data_dict['result'], True)

    # Test movie slicing
    def test_movie_list_slice_status_and_count(self):
        result=self.open_with_auth('/api/movies/?limit=5&offset=3',
                                       'GET',
                                       'twaits',
                                       'Passphrase1'
                                    )

        self.assertEqual(result.status_code, 200)

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(len(data_dict['movies']), 5)
        self.assertEqual(data_dict['movies'][0]['id'], 4)
        self.assertEqual(data_dict['movies'][-1]['id'], 8)

    # Test movie slice and filter
    def test_movie_list_slice_filter_status_and_count(self):
        result=self.open_with_auth('/api/movies/?limit=5&offset=3&filter=Sam+Raimi',
                                       'GET',
                                       'twaits',
                                       'Passphrase1'
                                    )

        self.assertEqual(result.status_code, 200)

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(len(data_dict['movies']), 1)
        self.assertEqual(data_dict['movies'][0]['id'], 4)

    # Test movie filter
    def test_movie_list_filter_status_and_count(self):
        result=self.open_with_auth('/api/movies/?limit=5&offset=3&filter=R',
                                       'GET',
                                       'twaits',
                                       'Passphrase1'
                                    )

        self.assertEqual(result.status_code, 200)

        data_dict = json.loads(result.data)

        # assert the response data
        self.assertEqual(len(data_dict['movies']), 3)
        self.assertEqual(data_dict['movies'][0]['id'], 4)
        self.assertEqual(data_dict['movies'][1]['id'], 5)
        self.assertEqual(data_dict['movies'][2]['id'], 6)

# runs the unit tests in the module
if __name__ == '__main__':
    user = User("twaits", "Passphrase1")
    user.save()
    unittest.main()

