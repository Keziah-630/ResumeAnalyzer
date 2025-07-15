# ResumeAnalyzer

ResumeAnalyzer is a Django-based web application for analyzing resumes, matching them to jobs, and managing job applications. It features user authentication, resume upload and analysis, job posting, and AI-powered job matching.

## Features
- User registration, login, and profile management
- Resume upload, listing, and detailed view
- AI-powered resume analysis
- Job posting and application system
- Job matching based on resume content
- Admin dashboard for user and job management

## Project Structure
- `analyzer/` - Resume analysis logic and views
- `jobs/` - Job posting, application, and management
- `matcher/` - Job-resume matching logic
- `resumes/` - Resume upload, listing, and management
- `users/` - User authentication, profiles, and admin views
- `templates/` - Shared and app-specific HTML templates
- `static/` - Static files (CSS, JS, images)

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Deployment on Render

1. **Push your code to GitHub.**
2. **Sign up/log in to [Render](https://render.com/).**
3. **Create a new Web Service:**
   - Connect your GitHub repo.
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `gunicorn ResumeAnalyzer.wsgi:application`
   - Add environment variables:
     - `DJANGO_SETTINGS_MODULE=ResumeAnalyzer.settings`
     - `DEBUG=False`
     - `ALLOWED_HOSTS=<your-render-url>`
     - `SECRET_KEY=<your-secret-key>`
   - (Optional) Add a PostgreSQL database and update `settings.py` accordingly.
4. **Static Files:**
   - Add `whitenoise` to `requirements.txt` and `MIDDLEWARE` in `settings.py`.
   - Set `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')` in `settings.py`.
   - Add `python manage.py collectstatic` as a build command if needed.
5. **Visit your Render URL to see your app live!**

## Notes
- For production, set `DEBUG = False` and use strong, secret keys.
- Never commit sensitive credentials to your repository.
- For email features, configure environment variables for email credentials.

## License
This project is for educational/demo purposes. 