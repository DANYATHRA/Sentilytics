# Quick Deployment Guide

## TL;DR - Deploy in 10 Minutes

### Deploy to Render (Recommended)

1. **Generate a secure key:**
   - Visit https://djecrety.ir/ and copy the generated key

2. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/sentilytics.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy on Render:**
   - Go to https://render.com → Sign up/Login
   - Click **New +** → **Web Service**
   - Connect your GitHub repo
   - Set **Start Command**: `cd backend && gunicorn youtube_audience_analyzer.wsgi:application --bind 0.0.0.0:$PORT`
   - Add environment variables:
     - `SECRET_KEY`: (from djecrety)
     - `DEBUG`: `False`
     - `PYTHON_VERSION`: `3.11.7`
     - `ALLOWED_HOSTS`: `your-app.onrender.com`
   - Click **Create Web Service**
   - Wait 5-10 minutes ✅

---

### Deploy to Vercel (Frontend Only or Serverless Django)

#### Option A: Frontend Only (Requires API Backend)

1. Separate frontend into a Next.js/React project
2. Deploy to Vercel with API_URL pointing to your Render backend
3. Set environment variable: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

#### Option B: Serverless Django on Vercel

1. Push to GitHub
2. Go to https://vercel.com → Import project
3. Set root directory to `backend`
4. Add same environment variables as Render
5. Deploy ✅

---

## Configuration Files Included

Your project now includes:

- ✅ `.gitignore` - Prevents sensitive files from being committed
- ✅ `.env.example` - Example environment variables
- ✅ `build.sh` - Build script for Render
- ✅ `render.yaml` - Render deployment config
- ✅ `vercel.json` - Vercel deployment config
- ✅ Updated `settings.py` - Production-ready Django settings

---

## Environment Variables Quick Reference

| Variable | Example | Required |
|----------|---------|----------|
| `SECRET_KEY` | From djecrety.ir | ✅ Yes |
| `DEBUG` | `False` | ✅ Yes |
| `ALLOWED_HOSTS` | `your-app.onrender.com,yourdomain.com` | ✅ Yes |
| `PYTHON_VERSION` | `3.11.7` | For Render |

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'whitenoise'"
**Solution:** Run: `pip install whitenoise`

### Issue: Static files not loading
**Solution:** 
- Run: `python manage.py collectstatic`
- Check `STATICFILES_DIRS` points to `frontend/static`
- Check `STATIC_ROOT` is set to `backend/staticfiles`

### Issue: "Connection refused" when trying to access database
**Solution:** 
- Run: `python manage.py migrate` in deployment environment
- For Render, use Dashboard → Console → Run command

### Issue: "CSRF token missing"
**Solution:** Ensure CSRF middleware is in settings.py (should be by default)

---

## Post-Deployment Checklist

After deployment, run these commands in your deployment shell:

```bash
# 1. Create superuser (for admin access)
python manage.py createsuperuser --noinput --username admin --email admin@example.com

# 2. Verify migrations
python manage.py migrate

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Test the application
curl https://your-app.onrender.com
```

---

## Useful Links

- 🔗 [Render Documentation](https://render.com/docs)
- 🔗 [Vercel Documentation](https://vercel.com/docs)
- 🔗 [Django Deployment Guide](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- 🔗 [Generate Secret Key](https://djecrety.ir/)
- 🔗 [WhiteNoise Documentation](http://whitenoise.evans.io/)

---

## Next Steps

1. **Local Testing:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Create `.env` file** (copy from `.env.example`)

3. **Push to GitHub**

4. **Deploy to Render or Vercel**

5. **Monitor deployment** in platform dashboard

For detailed deployment guide, see [DEPLOYMENT.md](DEPLOYMENT.md)
