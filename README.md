# tripsplit-backend
Travel expense sharing API — Django REST Framework

## Local Development with Docker

Build and start the local stack:

```powershell
docker compose up --build
```

Run database migrations:

```powershell
docker compose exec web python manage.py migrate
```

Run tests inside the web container:

```powershell
docker compose exec web python manage.py test accounts trips expenses
```

Check health endpoints:

```powershell
curl http://localhost:8000/healthz
curl http://localhost:8000/readyz
```

Stop containers:

```powershell
docker compose down
```

Stop containers and remove local PostgreSQL data volume:

```powershell
docker compose down -v
```

`docker compose down -v` removes the local PostgreSQL volume and deletes local database data. Use it only when you intentionally want a clean database.