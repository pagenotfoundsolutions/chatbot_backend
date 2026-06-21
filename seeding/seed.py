import json
import os
import sys

# Add project root to path so 'app' module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.shared.database.session import SessionLocal

from app.modules.ai_providers.adapters.output.persistence.sqlalchemy_provider_repository import SqlAlchemyProviderRepository
from app.modules.ai_providers.adapters.output.persistence.sqlalchemy_model_repository import SqlAlchemyModelRepository

from app.modules.ai_providers.application.commands.create_provider_handler import CreateProviderHandler
from app.modules.ai_providers.application.commands.create_model_handler import CreateModelHandler
from app.modules.ai_providers.application.commands.bulk_create_providers_handler import BulkCreateProvidersHandler
from app.modules.ai_providers.application.ports.input.bulk_create_providers_use_case import BulkCreateProvidersCommand, BulkProviderItemCommand

def seed_database(json_file_path: str):
    print(f"Starting database seeding from {json_file_path} using Domain Use Cases...")
    
    if not os.path.exists(json_file_path):
        print(f"Error: {json_file_path} not found.")
        return

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    items_data = data.get("items", [])
        
    db: Session = SessionLocal()
    
    try:
        provider_repo = SqlAlchemyProviderRepository(db)
        model_repo = SqlAlchemyModelRepository(db)
        
        create_provider_handler = CreateProviderHandler(provider_repo)
        create_model_handler = CreateModelHandler(model_repo)
        bulk_create_handler = BulkCreateProvidersHandler(create_provider_handler, create_model_handler)
        
        # Clear existing data to make the seed script safely re-runnable (idempotent)
        from sqlalchemy import text
        db.execute(text("TRUNCATE TABLE ai_models, ai_providers CASCADE;"))
        db.commit()
        
        # Build commands
        items = []
        for item in items_data:
            items.append(BulkProviderItemCommand(
                provider=item.get("provider", {}),
                models=item.get("models", [])
            ))
            
        cmd = BulkCreateProvidersCommand(items=items)
        
        # Execute the Bulk Create Use Case
        bulk_create_handler.execute(cmd)
        
        db.commit()
        print("Database seeding completed successfully.")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "seed_ai_data.json")
    seed_database(json_path)
