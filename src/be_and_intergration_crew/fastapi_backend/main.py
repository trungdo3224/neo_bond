# Import necessary modules and components
# FastAPI for creating the API, Depends for dependency injection, HTTPException for error handling
# Session from SQLAlchemy for database interactions
# Import models and database setup from the current package
from fastapi import FastAPI
# Initialize the FastAPI app
app = FastAPI(title="Neo Bond API")
from routers import (
    users,
    ai_instances,
    conversations,
    messages,
    emotions,
    speech_inputs,
    ai_responses,
    mood_tracking,
)

# Include all routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(ai_instances.router, prefix="/api", tags=["ai_instances"])
app.include_router(conversations.router, prefix="/api", tags=["conversations"])
app.include_router(messages.router, prefix="/api", tags=["messages"])
app.include_router(emotions.router, prefix="/api", tags=["emotions"])
app.include_router(speech_inputs.router, prefix="/api", tags=["speech_inputs"])
app.include_router(ai_responses.router, prefix="/api", tags=["ai_responses"])
app.include_router(mood_tracking.router, prefix="/api", tags=["mood_tracking"])

# Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # React dev server
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



# Root endpoint to verify the server is running
@app.get("/")
def read_root():
    return {"message": "Welcome to Neo Bond API"}


# Add event handler for shutdown
@app.on_event("shutdown")
async def app_shutdown_event():
    print("Application shutdown")
