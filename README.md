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

## Run The App Locally

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

The app will start at `http://127.0.0.1:8000`.

## Optional Redis

If Redis is available, rate limits are shared across instances. Otherwise the app falls back to local memory.

```bash
cd backend
docker-compose up
```

The frontend is served by FastAPI at `/`, so you do not need a separate frontend server.

## Demo Credentials

- Username: `demo`
- Password: `demo123`

## API Endpoints

- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/protected-api`
- `GET /api/rate-limit/status`

## Notes

- The demo user is stored in-memory for simplicity.
- Replace the secret key and move credentials to a database for production use.
- On Vercel, the in-memory limiter is best-effort only. Use a hosted Redis instance for consistent cross-request limits.

## Deploy To Vercel

- `api/index.py` is the Vercel Python entrypoint.
- `vercel.json` includes the backend and frontend files in the deployment bundle.
- The frontend calls the API with same-origin relative URLs, so it works on the deployed domain without extra CORS setup.
