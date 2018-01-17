# Users

* curl -u twaits -i http://localhost:5000/api/users/
* curl -i -H "Content-Type: application/json" -X POST -d '{"user":"cwaits", "password":"Passphrase1"}' http://localhost:5000/api/users/
 
 curl -i -H "Content-Type: application/json" -X POST -d '{"msg":"this is first message"}' http://localhost:5000/messages/

* curl -u twaits:Passphrase1 -i http://localhost:5000/api/users/

# Movies

## Get

* curl -u twaits:Passphrase1 -i http://localhost:5000/api/movies/
* curl -u twaits:Passphrase1 -i http://localhost:5000/api/movies/2
* curl -u twaits:Passphrase1 -i http://localhost:5000/api/movies/24

## Post

* curl -u twaits:Passphrase1 -i -H "Content-Type: application/json" -X POST -d '{"rated":"R", "director":"Wes Anderson"}' http://localhost:5000/api/movies/
* curl -u twaits:Passphrase1 -i -H "Content-Type: application/json" -X POST -d '{"title":"The Royal Tenenbaums", "year":"2001"}' http://localhost:5000/api/movies/
* curl -u twaits:Passphrase1 -i -H "Content-Type: application/json" -X POST -d '{"actors": "", "awards": "", "country": "", "director": "Wes Anderson", "genre": "", "id": 11, "imdbRating": null, "language": "", "metascore": "", "plot": "", "poster": "", "rating": "R", "released": "", "runtime": "", "title": "The Royal Tenenbaums", "writer": "", "year": 2001 }' http://localhost:5000/api/movies/

## Put

* curl -u twaits:Passphrase1 -i -H "Content-Type: application/json" -X PUT -d '{"actors": null, "awards": null, "country": null, "director": "Wes Anderson", "genre": null, "id": 11, "imdbRating": null, "language": null, "metascore": null, "plot": null, "poster": null, "rating": 'R', "released": null, "runtime": null, "title": null, "writer": null, "year": 2001 }' http://localhost:5000/api2/movies/11
* curl -u twaits:Passphrase1 -i -H "Content-Type: application/json" -X PUT -d '{"title": null, "year": null, "director": "Wes Anderson" }' http://localhost:5000/api2/movies/11


## Delete

* curl -u twaits:Passphrase1 -i -X DELETE http://localhost:5000/api/movies/11

## Get with query Strings

* curl -u twaits:Passphrase1 -i http://localhost:5000/api/movies/?limit=5'&'offset=3
* curl -u twaits:Passphrase1 -i http://localhost:5000/api/movies/?limit=5'&'offset=3'&'filter=Sam+Raimi
* curl -u twaits:Passphrase1 -i http://localhost:5000/api/movies/?filter=R
