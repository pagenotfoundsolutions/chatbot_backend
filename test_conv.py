import asyncio
import uuid
from sqlalchemy.orm import Session
from app.shared.database.database import SessionLocal, engine, Base
from app.modules.chat.adapters.output.persistence.sqlalchemy_conversation_repository import SqlAlchemyConversationRepository
from app.modules.chat.domain.entities.conversation import Conversation
from app.shared.kernel.utils import utc_now

def test():
    db = SessionLocal()
    repo = SqlAlchemyConversationRepository(db)
    
    auth_user_id = uuid.uuid4()
    conv = Conversation.start(auth_user_id, "Test")
    
    file_id = uuid.uuid4()
    conv.attach_file(file_id)
    
    repo.save(conv)
    db.commit()
    
    conv_id = conv.id
    
    db.close()
    
    # New session
    db2 = SessionLocal()
    repo2 = SqlAlchemyConversationRepository(db2)
    loaded_conv = repo2.get(conv_id)
    
    print("Files in loaded conv:", loaded_conv.file_ids)
    
if __name__ == "__main__":
    test()
