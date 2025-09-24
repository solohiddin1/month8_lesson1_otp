This is a Django project for managing users (students and teachers) with OTP-based login and group/lesson management.

## Features

- User registration (students)  
- OTP login via email  
- Custom user model with phone number and email  
- Group and lesson management  
- File uploads (images & videos for lessons)  
- Swagger API documentation  

## Tech Stack

- Python 3.13  
- Django  
- Django REST Framework  
- SQLite (default DB)  
- Pydantic settings  
- Email backend for OTP  
- Optional: RabbitMQ for async tasks  

## Installation

1. Clone the repository:

### bash
git clone <repo-url>
cd <project-folder>

    Create a virtual environment and install dependencies:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

    Set up environment variables in .env:

EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
PHOTO_PATH=/media/photos/
DEFAULT_PHOTO_PATH=/media/default.jpg
VIDEO_PATH=/media/videos/
DEFAULT_VIDEO_PATH=/media/default.mp4

    Run migrations:

python manage.py migrate

    Start the development server:

python manage.py runserver

API Documentation

Swagger UI is available at:

http://127.0.0.1:8000/swagger/

Usage

    Register a student via /register_user/

    Login via /userlogin/ (OTP will be sent to email)

    Manage groups and lessons via /create_groups/ and /lessons/ endpoints

Notes

    Custom user model uses email as USERNAME_FIELD.

    Uploaded files are stored in MEDIA_ROOT paths defined in .env.

    Tokens are automatically deleted when a user is deleted.
