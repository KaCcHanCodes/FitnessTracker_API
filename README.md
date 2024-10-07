# Fitness Tracker API

This project is a Django and Django REST Framework-based Fitness Tracker API with token-based authentication for API requests that provide features like user authentication with simple JWT authentication, workout tracking, workout activity history, workout metrics calculation, and profile management.

## Features

- Simple JWT Authentication: Secure user access to the API, ensuring only authenticated users can view, create, or update workout information.
- Workout Activity Management: Users can track workout sessions with details like start time, end time, distance, duration, and calories burned.
- Workout Activity History: Users can view a display of all activities logged, including activity details like  Activity Type, Duration, Calories Burned, and Date.
- Workout Metrics Calculation: Users can view workout metrics over a specified date range, including total duration, distance, and calories burned.
- Profile Management: Users can update their profiles while authenticated via JWT.

## Getting Started

### Prerequisites

1. **Python 3.x** installed on your machine. ([Follow this tutorial for your OS](https://realpython.com/installing-python/))
2. **pip** (Python package installer) and **virtualenv** to manage dependencies. ([Read Here](https://ehmatthes.github.io/pcc/chapter_12/installing_pip.html))
3. **Postgresql** installed and configured to support GeoDjango. ([Read Here](https://docs.djangoproject.com/en/5.1/ref/contrib/gis/testing/#postgis))

### Installing

Follow these steps to set up the project locally:

1. Clone the Repository
   
```bash
git clone https://github.com/<your-username>/FitnessTracker_API.git
```

2. Create a virtual environment and activate it:

Create a virtual environment to isolate the project dependencies.

```bash
python3 -m venv .my_env # Creates the virtual environment
source .env/bin/activate  # On Linux/MacOS 
.env\Scripts\activate # On Windows
```

3. Install Dependencies
   
```bash
pip install -r requirements.txt
```

4. Set Up the Database

- Create a .env file in the project root and secure your project configurations and database credentials:

5. Apply migrations to set up the database schema.
   
```bash
python manage.py migrate
```

6. (Optionally) Create a superuser for accessing the Django Admin panel:
   
```bash
python manage.py createsuperuser
```

7. Run the Development Server

Start the Django development server.

```bash
python manage.py runserver
```

## Running Tests

You can explore and test the API endpoints using **Swagger**. In Swagger, you can easily view the available API routes, their expected inputs and outputs, and test them directly.

### Access Swagger UI

To access the Swagger UI for this project:

1. Start the Django server by running:
   
   ```bash
   python manage.py runserver
   ```
2. Open your browser and navigate to the following URL:

  ```bash
  http://127.0.0.1:8000/docs/
  ```
3. Once on the Swagger UI page, you can explore all the available API endpoints. You can try out requests like login, workout tracking, and metrics calculation directly in your browser.

### Using JWT Authentication in Swagger

Some endpoints require authentication via a JWT token. Follow these steps to authenticate:

1. Use the login endpoint to obtain a JWT token.
2. In the Swagger UI, click the Authorize button at the top of the page.
3. Enter your JWT token in the following format:

   ```bash
   Bearer <your_token_here>
   ```
4. After authorizing, you will have access to authenticated endpoints (e.g., updating profile or workout data).

## Note

Make sure your Django server is running before accessing the Swagger UI.

   
