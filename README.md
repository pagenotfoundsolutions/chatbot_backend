# Chatbot (PDF RAG)

A chatbot backend service utilizing Retrieval-Augmented Generation (RAG) to interact with uploaded PDF documents. 

## Running the Application with Docker

This project uses Docker Compose to manage its services, including the FastAPI backend, PostgreSQL database, and pgAdmin. 

The environment variables are stored in the `env/` directory. By default, there are `.env.dev` and `.env.prod` files.

### Development Environment

To start the application in development mode (with hot-reloading enabled):

1. From the root of your project, run the following command:
   ```bash
   docker compose --env-file env/.env.dev -f docker/docker-compose.dev.yml up -d --build
   ```

### Production Environment

To start the application in production mode:

1. From the root of your project, run the following command:
   ```bash
   docker compose --env-file env/.env.prod -f docker/docker-compose.prod.yml up -d --build
   ```

### Accessing the Services

Once the containers are up and running, you can access the following services:

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **pgAdmin (Database GUI)**: http://localhost:5050 (Login with credentials specified in your `.env` file)
- **PostgreSQL Database**: Accessible internally at `db:5432` or via `localhost:5432` from your host machine.

### Database Migrations

This project uses Alembic for database schema migrations. Because the app runs inside Docker, you should run Alembic commands inside the `app` container.

**1. Generate an Automatic Migration**
If you modified your SQLAlchemy models (`models.py`) and want Alembic to automatically detect changes and generate a migration file:
```bash
docker compose --env-file env/.env.dev -f docker/docker-compose.dev.yml exec app alembic revision --autogenerate -m "describe_your_changes"
```

**2. Generate a Manual / Empty Migration**
If you need to write custom SQL (e.g., migrating data, complex constraints, or fixing `NOT NULL` on existing columns before adding them):
```bash
docker compose --env-file env/.env.dev -f docker/docker-compose.dev.yml exec app alembic revision -m "manual_changes"
```
*After generating, edit the new file in `alembic/versions/` to add your custom `op.execute(...)` or schema changes.*

**3. Apply Migrations (Upgrade)**
To apply any new migrations to your database:
```bash
docker compose --env-file env/.env.dev -f docker/docker-compose.dev.yml exec app alembic upgrade head
```

### Database Seeding

To pre-populate the database with initial data (like supported AI Providers and Models), a local Python script leverages the application's domain use cases directly. Since the application runs within Docker, execute the command via `docker compose`:

```bash
docker compose --env-file env/.env.dev -f docker/docker-compose.dev.yml exec app python seeding/seed.py
```
This script reads from `seeding/seed_ai_data.json` and cleanly populates the PostgreSQL database.
