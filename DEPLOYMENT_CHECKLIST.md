# Pre-Deployment Checklist

✅ **Project Structure:**
- [x] Separated frontend and backend folders
- [x] Backend folder contains: manage.py, requirements.txt, Django app
- [x] Frontend folder contains: templates/, static/

✅ **Configuration Files Created:**
- [x] `.gitignore` - Git ignore rules
- [x] `.env.example` - Environment variable template
- [x] `build.sh` - Build script for Render
- [x] `render.yaml` - Render deployment config
- [x] `vercel.json` - Vercel deployment config
- [x] `requirements.txt` - Updated with deployment dependencies
- [x] `settings.py` - Updated for production

✅ **Django Settings Updated:**
- [x] Environment variables support (decouple)
- [x] WhiteNoise middleware added for static files
- [x] ALLOWED_HOSTS configured from environment
- [x] SECRET_KEY from environment variable
- [x] DEBUG mode from environment variable
- [x] Static files configuration with STATIC_ROOT and STATIC_URL
- [x] Production settings (SSL, HSTS, secure cookies - all configurable)

✅ **Dependencies Added:**
- [x] `python-decouple==3.8` - Environment variable management
- [x] `dj-database-url==2.1.0` - Database URL parsing
- [x] `gunicorn==21.2.0` - Production WSGI server
- [x] `whitenoise==6.6.0` - Static files serving

---

## Deployment Steps by Platform

### For Render:

```
1. Generate SECRET_KEY from https://djecrety.ir/
2. Initialize Git and push to GitHub
3. Connect GitHub to Render
4. Set environment variables in Render dashboard
5. Deploy using build.sh and gunicorn start command
```

### For Vercel:

```
1. Generate SECRET_KEY from https://djecrety.ir/
2. Push to GitHub
3. Import project in Vercel
4. Set root directory to 'backend'
5. Configure environment variables
6. Deploy
```

---

## Files to Commit to Git

```bash
backend/
frontend/
.gitignore
.env.example          # ← Never commit actual .env
build.sh
render.yaml
vercel.json
DEPLOYMENT.md
QUICK_DEPLOY.md
README.md
```

## Files to NOT Commit (Already in .gitignore)

```
.env                  # Never commit with real values
db.sqlite3
*.pyc
__pycache__/
.venv/
venv/
```

---

## Quick Reference: Environment Variables

| Platform | SECRET_KEY | DEBUG | ALLOWED_HOSTS | PYTHON_VERSION |
|----------|-----------|-------|---------------|-----------------|
| **Render** | Required | `False` | `your-app.onrender.com` | `3.11.7` |
| **Vercel** | Required | `False` | `your-app.vercel.app` | Automatic |

---

## Commands to Run BEFORE Deployment

```bash
# Test locally
cd backend
python manage.py runserver

# Collect static files (important!)
python manage.py collectstatic --noinput

# Create .env file
cp .env.example .env
# Edit .env with your values

# Verify requirements.txt
pip install -r requirements.txt
```

---

## Commands to Run AFTER Deployment

```bash
# In your platform's shell (Render Dashboard or Vercel CLI)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files again (if needed)
python manage.py collectstatic --noinput

# Test the app
curl https://your-app.onrender.com
```

---

## Success Indicators

✅ App loads without errors  
✅ Admin panel accessible at `/admin`  
✅ Static files loading (CSS, JS, images)  
✅ Database migrations completed  
✅ Superuser created and can login  
✅ API endpoints responding correctly  

---

## Support Resources

📖 [Full Deployment Guide](DEPLOYMENT.md)  
⚡ [Quick Start Guide](QUICK_DEPLOY.md)  
📚 [Django Documentation](https://docs.djangoproject.com/)  
🚀 [Render Docs](https://render.com/docs)  
🔗 [Vercel Docs](https://vercel.com/docs)  

---

**Ready to deploy? Start with [QUICK_DEPLOY.md](QUICK_DEPLOY.md)**
