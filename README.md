# ecom

## Run locally

1. Create and activate Python virtualenv.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations and start server:

```bash
python ecom/manage.py migrate
python ecom/manage.py runserver
```

4. Open http://127.0.0.1:8000

## Free deployment (PythonAnywhere / Railway)

### PythonAnywhere (recommended free for Django)

1. Create free account at https://www.pythonanywhere.com
2. Upload project files or clone your repo.
3. In "Web" tab, create a new Django app.
4. Set source directory to `<your-root>/ecom` and WSGI to `ecom.wsgi`.
5. Put `ALLOWED_HOSTS = ['*']` in `ecom/ecom/settings.py` (for testing only).
6. Run `pip install -r requirements.txt` in Bash.
7. Reload web app and open your PythonAnywhere URL.

### Railway (free tier)

1. Sign up at https://railway.app and connect GitHub.
2. Add your repo and deploy.
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python ecom/manage.py runserver 0.0.0.0:$PORT`
5. Deploy and open the generated URL.

### Notes
- Keep sensitive keys out of repo (use environment variables).
- For production, use PostgreSQL or external DB.

## Quick deploy script

From project root (for Linux/Mac):

```bash
bash deploy.sh
```

For Windows PowerShell, run:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python ecom/manage.py migrate
python ecom/manage.py runserver
```
 
