# reto-faster

## Features

- FastAPI
- React
- SQLAlchemy and Alembic
- Docker images

## Good to know

The frontend of this project uses Boostrap.

## Step 1: Getting started

Start a local development instance with docker-compose

```bash
docker-compose up -d

Now you can navigate to the following URLs:

- Backend OpenAPI docs: http://localhost:9000/docs/
- Frontend: http://localhost:3000


Don't forget to edit the `.env` file and update the `BACKEND_CORS_ORIGINS` value (add `http://mydomain:3000` to the allowed origins).

### Rebuilding containers

If you add a dependency, you'll need to rebuild your containers like this:

```bash
docker-compose up -d --build
```


### Backend tests

The `Backend` service uses a hardcoded database named `apptest`. First, ensure that it's created

```bash
docker-compose exec postgres createdb apptest -U postgres
```

Then you can run tests with this command:

```bash
docker-compose run backend pytest --cov --cov-report term-missing
```
