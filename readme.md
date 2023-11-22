# FastAPI Template with MongoDB


This repository serves as a template for building FastAPI applications with MongoDB integration. It provides a basic project structure and configuration to help you get started quickly.

## Features

- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.9+.
- Docker: Containerization support using Docker and Docker Compose.
- MongoDB: Integration with MongoDB using `pymongo`.
- JWT Authentication: JSON Web Token-based authentication using `PyJWT`.
- CORS: Cross-Origin Resource Sharing middleware.
- Logging: Basic logging configuration.

## Requirements

- Python 3.9 or higher
- Docker (optional)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/officialalikhani/Fastapi-Template.git

Change into the project directory:

    cd your-fastapi-project
```

Create a virtual environment (optional but recommended):
```bash

    python3 -m venv .venv
    source .venv/bin/activate
```

Install the dependencies:
```bash
    pip install -r requirements.txt
```

Configuration

    Copy the example environment file and update the values:
    ```bash

    cp .env.example .env
    ```

    Update the .env file with your desired configuration settings, including the MongoDB connection details.

Usage

    Start the application server:
    ```bash

    python3 main.py
    ```

    The API should now be accessible at `http://localhost:YourPort`.

    Open your web browser and navigate to http://localhost:YourPort/docs to view the automatically generated API documentation.

Docker

You can also run the application using Docker. Make sure you have Docker installed and running on your machine.

Build the Docker image:
    ```bash

    docker-compose build
```

Start the Docker containers:
```bash

    docker-compose up -d
```

Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

Feel free to customize the README.md file further according to your specific needs and requirements.