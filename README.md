# Quake3 log parser

![CI/CD Status](https://github.com/elrf3lipes/quake3_log_parser/actions/workflows/ci-cd.yml/badge.svg)

## Overview

This project is a Quake 3 Arena log parser designed to read and analyze game log files. It provides functionalities to parse logs, track game statistics, and generate detailed reports. 
Application is modular and dockerized with integrated FastAPI for easy deployment and scalability, along with Github workflow for CI/CD practices.

## Project Structure

```
Quake3_log_parser
├── .github
│   └── workflows
│       └── ci-cd.yml - CI/CD configuration file.
├── .pytest_cache
├── quake_api
│   ├── __init__.py
│   └── main.py - FastAPI endpoints to interact with instantly fetched and parsed log data.
├── quake_parser
│   ├── __init__.py
│   ├── quake_log_parser.py - Coordinates log parsing and report generation.
│   ├── quake_log_utils.py - Contains utility functions for parsing log data.
│   └── reporting.py - Generates reports and rankings from parsed game data.
├── tests
│   ├── __init__.py
│   ├── test_log.txt - Test data file for verifying parsing functionality.
│   └── test_quake_log_utils.py - Unit tests for the Quake log parsing utilities.
├── venv
├── .dockerignore
├── .gitignore
├── Dockerfile
├── quake_log.txt - Example log file used for local development.
└── requirements.txt
```

## Features

- **Log Parsing**: Python `RegEx` module to extract match data from Quake 3 Arena logs.
- **Data Handling**: `DirectDict` for efficient data management.
- **Statistics Tracking**: Keeps track of kills, deaths, and other match statistics.
- **Handling `<world>` and Self-Kills**: Adjusts player scores for kills by `<world>` and self-kills based on the Quake 3 Arena -1 frag behavior, where players lose a frag for deaths not caused by other players.
- **Reporting**: Generates match reports and player rankings for all games.
- **CI/CD Pipeline**: Automated build, test, and deployment processes are managed via GitHub Actions, ensuring continuous integration and delivery.

## Dockerization

The application is dockerized to simplify deployment. To build and run the Docker container:

1. **Build the Docker Image**:
    ```sh
    docker build -t quake_log_parser .
    ```

2. **Run the Docker Container**:
    ```sh
    docker run -p 8000:8000 quake_log_parser
    ```

## FastAPI Application Documentation

### Overview

FastAPI application was created to provide endpoints for uploading, parsing logs, and retrieving various statistics. The API directly accesses and processes log files from the GitHub [Gist](https://gist.github.com/cloudwalk-tests/be1b636e58abff14088c8b5309f575d8), with parsed data stored in a temporary global cache.

### Endpoints

- **POST /parse_log** - Uploads and parses a log files.
- **GET /download_and_parse** - Download a log file from GitHub Gist, parses it, and deletes the file.
- **GET /player_kills** - Show player kills statistics for all games.
- **GET /means_usage** - Show usage statistics of different kill means for all games.
- **GET /total_kills** - Responds with the total number of kills for all games.
- **GET /used_means_by_player** - List means of death used by each player for all games.

### Responses

- `200 OK`: Successful request; returns the requested data.
- `400 Bad Request`: Invalid request or log file contents.
- `404 Not Found`: Requested resource not found.
- `500 Internal Server Error`: Unexpected error during processing.


## Setup and Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/elrf3lipes/quake3_log_parser
    cd quake3_log_parser
    ```

2. **Create and Activate a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the FastAPI Application**:
    ```sh
    uvicorn quake_api.main:app --reload
    ```

5. **Interactively Test the API**:
    - **Swagger UI**: Open interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
    - **ReDoc**: View detailed API documentation at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

6. **Run Tests**:
    ```sh
    pytest
    ```
    

## Notes

- The project includes asynchronous processing to handle large log files efficiently, though performance gains may not be significant with smaller files.
- Player ranking is based on kill count. Players with the same number of kills are ordered by their appearance in the log as per Quake3 rules.
- `<world>` and self-kills are handled according to the -1 frag behavior, where a player loses a frag for deaths not caused by other players, these still count in the total_kills

## Contribution

Feel free to contribute by opening issues or submitting pull requests. 

## License

This project is licensed under the MIT License.

---

For more details, check out the individual scripts or contact the project maintainer.
