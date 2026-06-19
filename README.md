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

If you need to run initial database migrations using Alembic after spinning up the containers for the first time, you can execute:
```bash
uv run alembic upgrade head
```


docker compose --env-file env/.env.dev -f docker/docker-compose.dev.yml exec app uv run alembic upgrade head



git config user.name "Adesh Yadav" && git config user.email "adeshyadav1145@gmail.com" && git add -f env/.env.example && git add . && git commit -m "Dockerize app, migrate to PostgreSQL, and extract environment config"