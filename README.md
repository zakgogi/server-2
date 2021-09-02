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
| /./:game_id | not aplicable                                         | Return game configuration for specific id                 | GET   |
| /./:game_id/scores | name of gamer and score of gamer                                        |  update the scores of a game with a new one                        | PATCH   |
| /./:game_id/scores | not aplicable | Return updated scores (not whole object)                  | GET   |
