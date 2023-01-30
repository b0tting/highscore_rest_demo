# highscorer
A python server and client for a simple RESTful API implementation. This is demonstration code. 

This RESTful server app has a few components to play with: 
- A REST [server] in both straight SQL and sql_alchemy variants that registers high scores for a given game name. 
- A [demo web page] with JQuery and one with Javascript with a fancy star field showing a continually updated list of highscores. 
 
# Highscore server
The highscore server comes in two flavors:
- highscore_server_barebones_on_db.py is a basic SQLite with SQL based implementation
- highscore_server_barebones_on_sqlalch.py is a SQLAlchemy using SQLite implementation

## Installing
To start the server, first make sure the requirements are installed: 
```
pip install -r requirements.txt
```
..then start for example the SQL based server:
```
python highscore_server_barebones_on_db.py
```
(and leave the process running!)

By default we listen on **all interfaces** (ie. 0.0.0.0) and **port 8080**. To start with a different port or a specific listener IP, add these to the start command as following:
```
python highscore_server.py 127.0.0.1:5000
```

## Usage
The highscore server takes highscores based on a game name using a REST API approach. Scores are saved in a local file called "highscore.json". The following URLs are available:

| URI | HTTP Verb | Description | 
| --- | --- | --- | 
| /highscores | GET | Lists all games known to the highscore server | 
| /highscores/\<gamename\> | GET | Given a \<gamename\>, retrieve the highscores known for that game. | 
| /highscores/\<gamename\> | POST | Expects a \<gamename\> and a body containing a dictionary with a name and a score, Only the top 10 scores are retained. Return a ranking if the score is in the top 10 (and a list of scores) or a 0 if your score did not make the top 10. | 

The body for the POST / save score method should resemble the following structure:
```json
{
    "name": "Mark",
    "score": 99
}
```
There's also a [Postman](https://www.postman.com/) file ([postman_collection.json](postman_collection.json)) you can use to test your server from Postman, just import it and modify the URL where required.

# Demo web page
The demo page is a fancy scrolling star field (https://github.com/jakesgordon/javascript-starfield/) with a list of highscores. There are 2 variants:
- A Jquery based approach 
- An ES2017-ES2020 pure javascript variant

You can run this page from your web browser directly but be aware of CORS. 
