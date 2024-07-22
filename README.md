# LocationService

This is a LocationService REST API, providing a backend for processing location data, including fetching addresses and calculating distances between points.

## Running the Service

You can run the LocationService in two ways:

### Using Docker Compose

1. Navigate to the `devops` folder.
2. Run `docker-compose up` to start the services.

### Running Locally

To run the project locally with a PostgresDB:

1. Install dependencies: `pipenv install`.
2. Activate the virtual environment (if needed): `pipenv shell`.
3. Start the flask service: `python app.py runserver`.
4. Start the worker service: `python app.py run_aiohttp_worker`.

## Short API Description

The service offers several endpoints for managing locations and processing tasks:

- `/location/calculate_distances/`: Upload a CSV file to calculate distances between points. Requires Basic Auth.
- `/location/distances_task/<task_id>/`: Retrieve the result of a distance calculation task. Requires Basic Auth.

## Contributions

Contributions to the LocationService project are welcome. Please ensure that your code adheres to the project's coding standards and include tests for new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
