# SubStream

SubStream is a Django-based application for video processing and subtitle extraction. It allows users to upload videos, extract subtitles in multiple languages, and search through the subtitles for specific words. The project uses Redis and Celery for background task processing, PostgreSQL for database management, and Docker for containerization.

## Technologies

- **Django**: Backend framework for building the web application.
- **PostgreSQL**: Database management system.
- **Redis**: Caching and message broker for Celery.
- **Celery**: Distributed task queue for background processing.
- **Docker**: Containerization for easy deployment and consistent environments.

## Features

- Upload videos and extract subtitles in multiple languages.
- Search subtitles for specific words and jump to the exact moment in the video where the word appears.
- Supports background task processing using Celery and Redis.
- PostgreSQL database to store video and subtitle information.

---

## Setup Instructions

### Prerequisites

Make sure you have the following installed:
- **Docker** (if running with Docker)
- **Python 3.x** (if running without Docker)
- **Redis** (for Celery task processing)

---

### Running the Project with Docker

#### Option 1: Build Locally

1. **Install Redis**:
   - On Linux: Run the following command to install Redis:
     ```bash
     sudo apt-get install redis-server
     ```
   - On Windows: Use the [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install) or install [Redis for Windows](https://github.com/MicrosoftArchive/redis/releases).
   
   - Start Redis using this command:
     ```bash
     sudo systemctl start redis
     ```

2. **Build and Run the Docker Container**:
   - Create a Docker image and run the project using the following commands:
     ```bash
     docker-compose --env-file video_processing/.env --build
     docker-compose up
     ```
   - Alternatively, combine both commands:
     ```bash
     docker-compose --env-file video_processing/.env up --build
     ```

#### Option 2: Use Public Docker Images

1. **Pull the Prebuilt Docker Images**:
   - You can pull the prebuilt Docker images directly from Docker Hub:
     ```bash
     docker pull lesanabbas/substream-celery
     docker pull lesanabbas/substream
     ```

2. **Run the Docker Containers**:
   - After pulling the images, run the containers using `docker-compose`:
     ```bash
     docker-compose --env-file video_processing/.env up
     ```

---

### Running the Project Without Docker

1. **Create a Virtual Environment**:
   - Create a virtual environment using the following command:
     ```bash
     python -m venv venv
     ```

2. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```

3. **Install Required Packages**:
   - Install all dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```

4. **Install Redis**:
   - On Linux: 
     ```bash
     sudo apt-get install redis-server
     ```
   - On Windows: Use the [Windows Subsystem for Linux (WSL)] or install [Redis for Windows](https://github.com/MicrosoftArchive/redis/releases).

5. **Start Redis**:
   - On Linux:
     ```bash
     sudo systemctl start redis
     ```
   - On Windows, follow the Redis installation guide to start the service.

6. **Run Celery and Django Server**:
   - Open two terminal windows:
     - **First terminal (Celery)**:
       ```bash
       celery -A video_processing worker --loglevel=info
       ```
     - **Second terminal (Django server)**:
       ```bash
       python manage.py runserver
       ```

---

## Project Structure

```bash
SubStream/
├── video_processing/          # Django app for video processing and subtitle extraction
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker configuration for running the project
├── .env                       # Environment variables file
└── README.md                  # Project documentation
