# Deployment Guide - Sentilytics

This guide provides step-by-step instructions to deploy your Sentilytics project to both **Render** and **Vercel**.

## Deployment Options

Your project can be deployed using one of these approaches:

### Option 1: Render (Recommended for Django Backend)
Deploy your entire Django application (backend + frontend) to Render.

### Option 2: Render + Vercel
Deploy backend to Render and frontend to Vercel as a separate SPA (requires frontend refactoring).

### Option 3: Vercel Serverless
Deploy Django as serverless functions on Vercel (more complex, requires special setup).

---

## Option 1: Deploy to Render (Recommended)

### Prerequisites
- GitHub/GitLab account with your code
- Render account (https://render.com)
- Git initialized in your project

### Step 1: Prepare Your Project for Deployment

1. **Create a `.gitignore` file** in the root directory:
```
# Python
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
*.pot
/media
/staticfiles
db.sqlite3
*.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

2. **Update `backend/youtube_audience_analyzer/settings.py`** for production:

Add these settings at the end of the file:

```python
# Production Settings
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-app.onrender.com', 'localhost', '127.0.0.1']

# For production use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = False  # Set to True for development

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')

# HTTPS and Security
SECURE_SSL_REDIRECT = False  # Render handles this automatically
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Database configuration for production
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()
```

3. **Create `.env.example`** (for reference, never commit .env):
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-app.onrender.com
DATABASE_URL=sqlite:///db.sqlite3
```

4. **Update `requirements.txt`** with additional production dependencies:

Add these lines to `backend/requirements.txt`:
```
python-decouple==3.8
dj-database-url==2.1.0
python-dotenv==1.0.0
gunicorn==21.2.0
whitenoise==6.6.0
```

Then run in your backend folder:
```bash
pip install whitenoise
```

5. **Add WhiteNoise for static files** in `backend/youtube_audience_analyzer/settings.py`:

Add to MIDDLEWARE (after SecurityMiddleware):
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest of middleware
]
```

### Step 2: Create Render Configuration Files

1. **Create `build.sh`** in the root directory:
```bash
#!/usr/bin/env bash
set -o errexit

cd backend
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

2. **Create `render.yaml`** in the root directory:
```yaml
services:
  - type: web
    name: sentilytics
    env: python
    region: oregon
    plan: free
    buildCommand: bash build.sh
    startCommand: "cd backend && gunicorn youtube_audience_analyzer.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.7
```

### Step 3: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Sentilytics project"

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/sentilytics.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Step 4: Deploy on Render

1. Go to https://render.com and sign up/log in
2. Click **"New +"** and select **"Web Service"**
3. Connect your GitHub repository
4. Fill in the following details:
   - **Name**: sentilytics
   - **Environment**: Python 3
   - **Region**: Oregon (or your preferred region)
   - **Branch**: main
   - **Build Command**: Leave default or use `bash build.sh`
   - **Start Command**: `cd backend && gunicorn youtube_audience_analyzer.wsgi:application --bind 0.0.0.0:$PORT`

5. **Environment Variables**:
   - Click "Advanced" and add these variables:
     - `PYTHON_VERSION`: `3.11.7`
     - `SECRET_KEY`: Generate a new secure key at https://djecrety.ir/
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `your-app.onrender.com,yourdomain.com`

6. Click **"Create Web Service"**

7. Wait for deployment (5-10 minutes). Your app will be available at `https://your-app.onrender.com`

---

## Option 2: Deploy Frontend to Vercel + Backend to Render

This approach separates the frontend and backend.

### Prerequisites
- Vercel account (https://vercel.com)
- Render account (for backend)
- Node.js installed locally

### Step 1: Create Frontend SPA (React/Vue/Next.js)

For a basic static HTML site:

Create `frontend/next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
}

module.exports = nextConfig
```

Create `frontend/vercel.json`:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "out"
}
```

### Step 2: Deploy Backend to Render (Follow Option 1)

### Step 3: Deploy Frontend to Vercel

1. Push your frontend code to GitHub
2. Go to https://vercel.com and sign up/log in
3. Click **"Add New"** → **"Project"**
4. Import your GitHub repository
5. Select the `frontend` folder as root directory
6. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your Render backend URL (e.g., `https://sentilytics.onrender.com`)
7. Click **"Deploy"**

---

## Option 3: Deploy to Vercel with Serverless Functions

### Create `backend/vercel.json`

```json
{
  "version": 2,
  "builds": [
    {
      "src": "youtube_audience_analyzer/wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "youtube_audience_analyzer/wsgi.py"
    }
  ]
}
```

### Update requirements.txt

Add to `backend/requirements.txt`:
```
vercel==24.0.0
python-multipart==0.0.5
```

### Deploy

1. Push to GitHub
2. Go to Vercel and create a new project
3. Import your GitHub repository
4. Set root directory to `backend`
5. Add environment variables (SECRET_KEY, DEBUG, etc.)
6. Deploy

---

## Post-Deployment Steps

### 1. Database Migrations

After deployment, run migrations on the deployed instance:

**For Render:**
```bash
# SSH into your Render instance and run
python manage.py migrate
```

Or use Render Shell in the dashboard.

### 2. Create Superuser (for admin access)

```bash
python manage.py createsuperuser --noinput --username admin --email admin@example.com
```

(Set password via environment variable)

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Test Your Deployment

- Visit your deployed URL
- Check admin panel at `/admin`
- Test API endpoints

---

## Troubleshooting

### Static Files Not Loading
- Ensure `STATIC_URL = '/static/'` in settings.py
- Run `python manage.py collectstatic`
- Check that WhiteNoise is installed and in MIDDLEWARE

### Database Issues
- Use `python manage.py migrate` after deployment
- For Render, use managed PostgreSQL database if available

### Environment Variables Not Loading
- Check that `.env` file is NOT committed to git
- Add variables via platform dashboard (never in git)
- Use `python-decouple` to load them: `from decouple import config`

### Port Issues
- Ensure your app listens on `0.0.0.0:PORT` environment variable
- Don't hardcode port 8000

---

## Performance Optimization Tips

1. **Enable caching** for static files
2. **Use managed databases** instead of SQLite in production
3. **Enable GZIP compression** for responses
4. **Optimize images** in frontend
5. **Use CDN** for static assets (Render/Vercel provide this)

---

## Security Checklist

- [ ] Change SECRET_KEY (use https://djecrety.ir/)
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (automatic on Render/Vercel)
- [ ] Set secure cookie flags (SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE)
- [ ] Use strong database passwords
- [ ] Enable CSRF protection (default in Django)

---

## Useful Commands

### Local Development
```bash
cd backend
python manage.py runserver
```

### Create Static Files Build
```bash
python manage.py collectstatic
```

### Database Backup
```bash
python manage.py dumpdata > backup.json
```

### Load Data from Backup
```bash
python manage.py loaddata backup.json
```

## Support & Documentation

- **Render Documentation**: https://render.com/docs
- **Vercel Documentation**: https://vercel.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/6.0/howto/deployment/
