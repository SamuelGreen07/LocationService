# TicTacToeFlask

This is a TicTacToe Flask REST API service, providing a backend for a TicTacToe game with user authentication and game management.

## Running the Service

You can run the TicTacToeFlask service in two ways:

### Using Docker Compose

1. Navigate to the `devops` folder.
2. Run `docker-compose up` to start the services.

### Running Locally

To run the project locally with a PostgresDB:

1. Install dependencies: `pipenv install`.
2. Activate the virtual environment (if needed): `pipenv shell`.
3. Start the service: `python app.py runserver`.

## Short API Description

The service offers several endpoints for game management and user authentication:

- `/users/create_user/`: For user registration.
- `/users/user/`: Retrieve current user info. Requires Basic Auth.
- `/game/start_game/`: Initialize a new game or find an existing one if someone is waiting for a player. Requires Basic Auth.
- `/game/<game_id>/show_board/`: Show the game board in text format. Requires Basic Auth.
- `/game/<game_id>/make_move/`: Make a move in the game by choosing a row. Requires Basic Auth.

## Contributions

Contributions to the TicTacToeFlask project are welcome. Please ensure that your code adheres to the project's coding standards and include tests for new features.

## License