from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.models.speech_inputs import SpeechInput
from fastapi_backend.schemas.speech_inputs import SpeechInputSchema

class SpeechInputService:
    def __init__(self, db: Session):
        self.db = db

    def get_speech_inputs(self, skip: int = 0, limit: int = 10) -> List[SpeechInput]:
        return self.db.query(SpeechInput).offset(skip).limit(limit).all()

    def get_speech_input_by_id(self, input_id: str) -> Optional[SpeechInput]:
        return self.db.query(SpeechInput).filter(SpeechInput.id == input_id).first()

    def get_user_speech_inputs(self, user_id: str) -> List[SpeechInput]:
        return self.db.query(SpeechInput)\
            .filter(SpeechInput.user_id == user_id)\
            .order_by(SpeechInput.processed_at.desc())\
            .all()

    def get_conversation_speech_inputs(self, conversation_id: str) -> List[SpeechInput]:
        return self.db.query(SpeechInput)\
            .filter(SpeechInput.conversation_id == conversation_id)\
            .order_by(SpeechInput.processed_at.asc())\
            .all()

    def create_speech_input(self, speech_input: SpeechInputSchema) -> SpeechInput:
        db_speech_input = SpeechInput(**speech_input.dict())
        self.db.add(db_speech_input)
        self.db.commit()
        self.db.refresh(db_speech_input)
        return db_speech_input

    def update_speech_input(self, input_id: str, speech_input: SpeechInputSchema) -> Optional[SpeechInput]:
        db_speech_input = self.get_speech_input_by_id(input_id)
        if not db_speech_input:
            return None
        
        # Update speech input fields
        for key, value in speech_input.dict(exclude_unset=True).items():
            setattr(db_speech_input, key, value)
        
        self.db.commit()
        self.db.refresh(db_speech_input)
        return db_speech_input

    def delete_speech_input(self, input_id: str) -> Optional[SpeechInput]:
        speech_input = self.get_speech_input_by_id(input_id)
        if not speech_input:
            return None
        
        self.db.delete(speech_input)
        self.db.commit()
        return speech_input
