# Quake3 log parser

![CI/CD Status](https://github.com/elrf3lipes/quake3_log_parser/actions/workflows/ci-cd.yml/badge.svg)

## Overview

This project is a Quake 3 Arena log parser designed to read and analyze game log files. It provides functionalities to parse logs, track game statistics, and generate detailed reports. 
The application is dockerized for easy deployment and scalability.

## Project Structure

- **`.github/workflows/ci-cd.yml`**: CI/CD configuration file.
- **`.pytest_cache/`**: Pytest cache directory.
- **`quake_api/main.py`**: FastAPI application with endpoints to interact with parsed log data.
- **`venv/`**: Virtual environment directory.
- **`.dockerignore`**: Docker ignore file.
- **`.gitignore`**: Git ignore file.
- **`Dockerfile`**: Dockerfile for containerizing.
- **`quake_log.txt`**: Example log file used for local development.
- **`quake_log_parser.py`**: Coordinates log parsing and report generation.
- **`quake_log_utils.py`**: Contains utility functions for parsing log data.
- **`reporting.py`**: Generates reports and rankings from parsed game data.
- **`requirements.txt`**: Python dependencies.
- **`test_log.txt`**: Test data file for verifying parsing functionality.
- **`test_quake_log_utils.py`**: Unit tests for the Quake log parsing utilities.

## Features

- **Log Parsing**: Uses Python's `re` module to extract match data from Quake 3 Arena logs.
- **Data Handling**: Utilizes `DirectDict` for efficient data management.
- **Statistics Tracking**: Keeps track of kills, deaths, and other match statistics.
- **Handling `<world>` and Self-Kills**: Adjusts player scores for kills by `<world>` and self-kills based on the Quake 3 Arena -1 frag behavior, where players lose a frag for deaths not caused by other players.
- **Reporting**: Generates match reports and player rankings.

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

This FastAPI application provides endpoints for parsing and analyzing Quake log files. It supports uploading and parsing logs, downloading logs from a remote source, and retrieving various statistics. 
The API directly accesses and temporarily processes the log file from a GitHub Gist. A global cache dictionary stores the parsed log data keyed by the file path, which is used by all endpoints. 
The cache is updated when a new log file is parsed and eventually deleted after processing.

### Endpoints

1. **POST /parse_log**
   - **Description**: Upload and parse a log file.
   - **Request Body**:
     ```json
     {
       "file_path": "path_to_log_file"
     }
     ```
   - **Responses**:
     - `200 OK`: Returns the parsed game data.
     - `404 Not Found`: If the log file does not exist.
     - `400 Bad Request`: For invalid log file contents.
     - `500 Internal Server Error`: For unexpected errors.

2. **GET /download_and_parse**
   - **Description**: Downloads a log file from a GitHub Gist, parses it, and deletes the file.
   - **Responses**:
     - `200 OK`: Returns the parsed game data.
     - `500 Internal Server Error`: For errors during download, parsing, or file operations.

3. **GET /player_kills**
   - **Description**: Retrieves and returns player kill statistics from the cached log data.
   - **Responses**:
     - `200 OK`: Returns player kill statistics sorted by number of kills.
     - `500 Internal Server Error`: For issues with parsing or accessing cached data.

4. **GET /means_usage**
   - **Description**: Retrieves and returns the usage statistics of different kill means from the cached log data.
   - **Responses**:
     - `200 OK`: Returns kill means usage sorted by count.
     - `500 Internal Server Error`: For issues with parsing or accessing cached data.

5. **GET /total_kills**
   - **Description**: Retrieves and returns the total number of kills from the cached log data.
   - **Responses**:
     - `200 OK`: Returns the total number of kills.
     - `500 Internal Server Error`: For issues with parsing or accessing cached data.

6. **GET /used_means_by_player**
   - **Description**: Retrieves and returns the means of death used by each player from the cached log data.
   - **Responses**:
     - `200 OK`: Returns means used by each player, sorted by frequency.
     - `500 Internal Server Error`: For issues with parsing or accessing cached data.


## Setup and Installation

1. **Clone the Repository**:
    ```sh
    git clone <repo-url>
    cd CloudWalk_Assessment
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

5. **Run Tests**:
    ```sh
    pytest
    ```

## Notes

- The project includes asynchronous processing to handle large log files efficiently, though performance gains may not be significant with smaller files.
- Player ranking is based on kill count. Players with the same number of kills are ordered by their appearance in the log. 
- After much consideration(and a bit of indecision..) I've decided to take into consideration quake3 arena rule called the -1 frag behavior, which was introduced to prevent people from deliberately suiciding when near death. 
People would do that in order to deny a frag to another player. If you die by any means other than another player killing you then you lose a frag.
- `<world>` and self-kills are handled according to the -1 frag behavior, where a player loses a frag for deaths not caused by other players, these still count in the total_kills

## Contribution

Feel free to contribute by opening issues or submitting pull requests. 

## License

This project is licensed under the MIT License.

---

For more details, check out the individual scripts or contact the project maintainer.
