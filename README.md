# Chatbot (PDF RAG)

A chatbot backend service utilizing Retrieval-Augmented Generation (RAG) to interact with uploaded PDF documents. 

## Running the Application with Docker

This project uses one Docker Compose file and one local `env/.env` file. It
connects to the PostgreSQL/pgvector container in `../shared-db`. Development
and production can use separate databases in that one container
(`chatbot_dev` and `chatbot_db`) without duplicating the database server.

Start the shared database first:

```bash
cd /home/adesh-yadav/Desktop/projects/shared-db
docker compose up -d --wait
```

Create the local environment once, edit its secrets, and start the app:

```bash
cp env/.env.example env/.env
docker compose --env-file env/.env -f docker/docker-compose.yml up -d --build --wait
```

Production values in `env/.env`:

```dotenv
APP_ENV=prod
APP_RELOAD=false
POSTGRES_DB=chatbot_db
APP_RUNTIME_MOUNT=app_uploads:/app/storage/uploads
```

For development, change only these values and run the same Compose command:

```dotenv
APP_ENV=dev
APP_RELOAD=true
POSTGRES_DB=chatbot_dev
APP_RUNTIME_MOUNT=../:/app
```

### Accessing the Services

Once the containers are up and running, you can access the following services:

- **API Documentation (Swagger UI)**: http://localhost:18100/api/docs
- **Health check**: http://localhost:18100/health
- **PostgreSQL from Docker**: `shared-postgres:5432`
- **PostgreSQL from the host**: `localhost:5432`

Switching modes recreates only the app container; the shared database remains
running.

### Database Migrations

This project uses Alembic for database schema migrations. Because the app runs inside Docker, you should run Alembic commands inside the `app` container.

**1. Generate an Automatic Migration**
If you modified your SQLAlchemy models (`models.py`) and want Alembic to automatically detect changes and generate a migration file:
```bash
docker compose --env-file env/.env -f docker/docker-compose.yml exec app alembic revision --autogenerate -m "describe_your_changes"
```

**2. Generate a Manual / Empty Migration**
If you need to write custom SQL (e.g., migrating data, complex constraints, or fixing `NOT NULL` on existing columns before adding them):
```bash
docker compose --env-file env/.env -f docker/docker-compose.yml exec app alembic revision -m "manual_changes"
```
*After generating, edit the new file in `alembic/versions/` to add your custom `op.execute(...)` or schema changes.*

**3. Apply Migrations (Upgrade)**
To apply any new migrations to your database:
```bash
docker compose --env-file env/.env -f docker/docker-compose.yml exec app alembic upgrade head
```

### Database Seeding

To pre-populate the database with initial data (like supported AI Providers and Models), a local Python script leverages the application's domain use cases directly. Since the application runs within Docker, execute the command via `docker compose`:

```bash
docker compose --env-file env/.env -f docker/docker-compose.yml exec app python seeding/seed.py
```
This script reads from `seeding/seed_ai_data.json` and cleanly populates the PostgreSQL database.
