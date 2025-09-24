Public Records Notification System API
This repository contains the backend API for the Public Records Notification System, a SaaS application designed to provide automated, continuous monitoring of public records related to user-defined addresses.

The core of this system is a powerful, asynchronous scraping engine built with Python, FastAPI, and Celery that can be scaled to monitor data sources for thousands of addresses.

Features
JWT-Based Authentication: Secure user registration and login endpoints.

Protected Routes: Endpoints for managing addresses and viewing records are protected and require authentication.

Asynchronous Task Queuing: Uses Celery and Redis to run long-running scraping jobs in the background without blocking the API.

Modular, Data-Driven Scraping Engine: A robust scraper powered by Playwright that can be easily configured to target new data sources by simply adding a new configuration object.

Scalable Architecture: Designed to be horizontally scalable by running multiple Celery worker instances.

Production-Ready Foundation: Includes database models, API schemas, and a logical project structure.

Technology Stack
Language: Python 3.9+

API Framework: FastAPI

Asynchronous Tasks: Celery

Message Broker: Redis

Database: PostgreSQL

ORM: SQLAlchemy

Web Scraping: Playwright & BeautifulSoup4

Data Validation: Pydantic

Project Setup & Installation
Follow these steps to get the backend running locally.

1. Prerequisites
Python 3.9 or higher

PostgreSQL installed and running.

Redis installed and running.

2. Clone the Repository
git clone <your-repository-url>
cd public-records-api

3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment.

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

4. Install Dependencies
Install all required Python packages from the requirements.txt file.

pip install -r requirements.txt

5. Install Playwright Browsers
Playwright requires downloading browser binaries for automation. This is a one-time setup command.

playwright install

6. Configure Environment Variables
Create a .env file in the project root directory. This file is used to store sensitive information like database credentials and secret keys. Copy the contents of .env.example (you would create this file for your team) or use the template below.

Create a file named .env:

DATABASE_URL=postgresql://your_db_user:your_db_password@localhost/public_records
SECRET_KEY=a_very_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

Important: Make sure to replace the DATABASE_URL with your actual PostgreSQL connection string. You will also need to create the public_records database manually.

7. Run Database Migrations
You would use a tool like Alembic to manage your database schema.

# (Assuming Alembic is configured)
alembic upgrade head

Running the Application
To run the application, you need to start three separate services in three different terminal windows.

1. Terminal 1: Start the FastAPI Server

This command starts the web server. The --reload flag will automatically restart the server when you make code changes.

uvicorn app.main:app --reload

You can now access the interactive API documentation at http://127.0.0.1:8000/docs.

2. Terminal 2: Start the Celery Worker

This command starts a Celery worker, which will listen for and execute background tasks from the Redis queue.

celery -A app.worker.celery_app worker --loglevel=info

3. Terminal 3: (If Needed) Monitor with Flower

Flower is a real-time web-based monitor for Celery. It's very useful for debugging.

celery -A app.worker.celery_app flower

You can view the Flower dashboard at http://localhost:5555.
