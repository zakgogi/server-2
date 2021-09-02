## Endpoint routes USER

| Route          | Data Required from front end                                           | Description                                             | Type   |
| -------------- | ---------------------------------------------------------------------- | ------------------------------------------------------- | ------ |
| /register | username, password, email                                              | End of game for scores                 | GET   |
| /login    | username, password                                                     | Will be hit on login page                               | GET   |
| /        | habitname, times_completed = 0, frequency_day, streak = 0, username_id | Will be hit when creating new habits                    | GET   |
| /configuration        | id(habit_id), times_completed, frequency_day                           | Will be hit when user presses plus button on habit card | PATCH  |



## REST endpoint routes API

| Route          | Data Required from front end                                           | Description                                             | Type   |
| -------------- | ---------------------------------------------------------------------- | ------------------------------------------------------- | ------ |
| /./:game_id | not aplicable                                         | Return game configuration for specific id                 | GET   |
| /./:game_id/scores | name of gamer and score of gamer                                        |                               | PATCH   |
| /./:game_id/scores | not aplicable | Will be hit when creating new habits                    | GET   |
