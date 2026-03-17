# Sentilytics - Project Structure

This project is organized with separate frontend and backend folders.

## Project Structure

```
Sentilytics/
├── backend/                  # Django backend application
│   ├── manage.py            # Django management script
│   ├── db.sqlite3           # SQLite database
│   ├── requirements.txt      # Python dependencies
│   ├── youtube_audience_analyzer/  # Main Django project settings
│   ├── analyzer/            # Main Django app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services/        # Services for analysis
│   │   │   ├── sentiment_analysis.py
│   │   │   ├── comment_fetcher.py
│   │   │   ├── preprocessing.py
│   │   │   └── ...
│   │   └── migrations/
│   └── test_*.py            # Backend tests
│
├── frontend/                # Frontend assets
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   └── analyzer/
│   └── static/              # Static files (CSS, JS, images)
│
└── README.md               # This file
```

## Getting Started

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend

Frontend files (HTML templates and static assets) are located in the `frontend/` folder and are served by Django.

## Notes

- The Django `settings.py` has been configured to serve templates and static files from the `frontend/` folder.
- All backend Python code and configuration remains in the `backend/` folder.
- Database file (`db.sqlite3`) and `manage.py` are in the `backend/` folder.
