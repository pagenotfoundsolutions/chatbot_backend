import asyncio
from sqlalchemy import select
from app.shared.database.database import SessionLocal
from app.modules.ai_providers.adapters.output.persistence.models.ai_model_model import AIModelModel

def run():
    with SessionLocal() as db:
        models = db.scalars(select(AIModelModel)).all()
        for m in models:
            if "nemotron" in m.name.lower():
                print(f"Model: {m.name}, supports_tools: {m.supports_tools}")

run()
