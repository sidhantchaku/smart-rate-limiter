# Smart API Rate Limiter

A small fullstack starter built from the ZIP reference you shared.

## Stack

- Backend: FastAPI
- Auth: JWT login
- Rate limiting: Redis first, in-memory fallback
- Frontend: HTML, CSS, and vanilla JavaScript dashboard

## Project Structure

```text
backend/
  app/
    models/
    routes/
    services/
  main.py
  requirements.txt
  docker-compose.yml
frontend/
  index.html
  app.js
  styles.css
```

## Run The Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will start at `http://127.0.0.1:8000`.

## Optional Redis

If Redis is available, rate limits are shared across instances. Otherwise the app falls back to local memory.

```bash
cd backend
docker-compose up
```

## Frontend

Open `frontend/index.html` in a browser after the backend is running.

## Demo Credentials

- Username: `demo`
- Password: `demo123`

## API Endpoints

- `POST /auth/login`
- `GET /auth/me`
- `GET /protected-api`
- `GET /rate-limit/status`

## Notes

- The demo user is stored in-memory for simplicity.
- Replace the secret key and move credentials to a database for production use.
