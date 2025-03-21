Mentorship Platform

Project Overview:

The mentorship platform was designed to connect mentees and case managers, with two distinct user types: Mentees and Case Managers. Mentees can submit surveys and track their progress, while case managers can manage sessions, write reports, and view mentee surveys.

Framework: Django 5.1.4

Python Version: 3.11

Deployment Platform: Render

URL:https://django-starter-template.onrender.com 

Prerequisites

Python 3.11 installed locally

Git for version control

A Render account and a connected Git repository (e.g., GitHub)

Setup Instructions

Local Development

Clone the Repository:
git clone https://github.com/your-username/django-starter-template.git

cd django-starter-template

Create a Virtual Environment:

python -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Run Migrations:

python manage.py migrate

Start the Development Server:

python manage.py runserver

Visit http://localhost:8000/ in your browser.

Deployment on Render

Prepare the Project:

Ensure requirements.txt includes:
Django==5.1.4
gunicorn==20.1.0

Update config/settings.py:

ALLOWED_HOSTS = ['django-starter-template.onrender.com']
DEBUG = False  # Set to True for debugging, False for production
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
Collect static files locally to test: python manage.py collectstatic.

Push to Git:

git add .

git commit -m "Prepare for Render deployment"

git push origin main

Configure Render:
Service Type: Web Service
Environment: Python 3
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
Start Command: gunicorn config.wsgi:application

Environment Variables:

SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=django-starter-template.onrender.com
PYTHON_VERSION=3.11

Deploy:

Connect your GitHub repo in Render and create the service.
After deployment, run migrations via Render’s Shell:
python manage.py migrate


Troubleshooting
Gunicorn Not Found:

Error: bash: line 1: gunicorn: command not found

Fix: Ensure gunicorn is in requirements.txt and the build command runs pip install -r requirements.txt.

DisallowedHost Error:

Error: Invalid HTTP_HOST header: 'django-starter-template.onrender.com'

Fix: Add django-starter-template.onrender.com to ALLOWED_HOSTS in settings.py.

Static Files Not Serving:

Ensure collectstatic runs in the build command and STATIC_ROOT is set.

Additional Notes

Database: This template uses SQLite by default. For production, consider Render’s PostgreSQL service and configure with dj-database-url.

Auto-Deploys: Enabled by default in Render—pushing to main triggers a redeploy.

Custom Domains: Update ALLOWED_HOSTS if adding a custom domain via Render.

Contributing

Feel free to fork this repo, submit issues, or send pull requests to improve the template!
