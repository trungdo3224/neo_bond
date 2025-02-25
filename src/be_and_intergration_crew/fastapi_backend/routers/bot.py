from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_backend.schemas import models,database

router = APIRouter()
# Endpoint to create a new AI response log
# Accepts response_content as input
# Saves the response log to the database and returns the saved object'

# @router.post("/responses/")
# async def create_response(response_content: str, db: Session = Depends(database.get_db())):
#     response_log = models.AIResponseLog(response_content=response_content)
#     db.add(response_log)
#     db.commit()
#     db.refresh(response_log)
#     return response_log


# Endpoint to read AI response logs
# Supports pagination with skip and limit parameters
# Returns a list of AI response logs from the database

# @router.get("/responses/")
# async def read_responses(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db())):
#     responses = db.query(models.AIResponseLog).offset(skip).limit(limit).all()
#     return responses