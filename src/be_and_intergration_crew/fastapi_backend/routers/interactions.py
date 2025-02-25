import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_backend.schemas import database, models
from fastapi_backend.schemas.services import users_service

router = APIRouter()

# Endpoint to read user interactions
# Supports pagination with skip and limit parameters
# Returns a list of user interactions from the database
@router.get("/interactions/")
async def read_interactions(skip: int = 0, limit: int = 10, db: Session = databaseSession):
    interactions = db.query(models.UserInteraction).offset(skip).limit(limit).all()
    return interactions

# Endpoint to create a new user interaction
# Accepts user_id, interaction_type, and interaction_content as input
# Saves the interaction to the database and returns the saved object
@router.post("/interactions/")
async def create_interaction(user_id: str, interaction_type: str, interaction_content: str, db: Session = Depends(database.get_db)):
    """
    Create a new user interaction.

    Parameters:
    - user_id (str): The ID of the user.
    - interaction_type (str): The type of interaction.
    - interaction_content (str): The content of the interaction.
    - db (Session): The database session.

    Returns:
    - interaction: The saved UserInteraction object.
    """
    interaction = models.UserInteraction(user_id=user_id, interaction_type=interaction_type, interaction_content=interaction_content)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction