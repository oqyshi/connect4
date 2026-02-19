# Connect 4

## Running the Project

### Option 1: Docker Compose (recommended)  *

```bash
docker compose up
```

The app will be available at http://localhost:8000.
First run might take longer to create db file.

### Option 2: Local (runserver)

**Requirements:** Python 3.11+

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The app will be available at http://localhost:8000.
