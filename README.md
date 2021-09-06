## Installation

* Clone or download the repo.
* Open terminal and navigate to the project folder.
* Run pipenv shell to enter virtual environment (or virtual environment of your choice)
* Run pipenv install to install dependencies

### Usage

* Run docker-compose up on another terminal
* Run in the pipenv shell terminal pipenv run dev to launch
* Go to localhost:8000 to view the server app

## Endpoint routes USER

| Route          |  Description                                             |
| -------------- | ------------------------------------------------------- |
| /register |  show register (linked from client and login page)                 |
| /login    | Show Login page (home when nobody is logged in)
| /        | show the actual configuration of the game for that user and link to update config |
| /configuration        | Form to configurate the game or update |
| /settings | form to update user settings |



## REST endpoint routes API

| Route          | Data Required from front end                                           | Description                                             | Type   |
| -------------- | ---------------------------------------------------------------------- | ------------------------------------------------------- | ------ |
| /json/:game_id | not aplicable | Return game configuration for specific id | GET |
| /json/:game_id/scores | name of gamer and score of gamer |  update the scores of a game with a new one  | PATCH   |
| /json/:game_id/scores | not aplicable | Return updated scores (not whole object) | GET |
| /json/:wedding_url | not aplicable | Return two games ids with the character names |  
