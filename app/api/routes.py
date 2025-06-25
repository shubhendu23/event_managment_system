from fastapi import FastAPI, responses, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config.logger import Logger
from config.dto import EventDTO, EventCreateDTO, RegisterDTO, AttendeeDTO
from typing import List
from service.attendees import Attendees
from service.events import Events

logger = Logger().logger

app = FastAPI(title="Event Management Service",docs_url="/docs",
    redoc_url="/redoc", 
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; adjust in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/" )
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Event Management API"}

@app.get("/health",)
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

@app.get("/events", response_model=List[EventDTO])
async def get_events():
    try:
        logger.info("Fetching all events")
        events = await Events().get_events()
        return [EventDTO.from_orm(event) for event in events]   
    except Exception as e:
        logger.error(f"Error fetching events: {str(e)}")
        return responses.JSONResponse(
            status_code=500,
            content={"error": "An error occurred while fetching events"})
        # In a real application, you might want to raise an HTTPException here


@app.post("/events", response_model=EventDTO)
async def create_event(event: EventCreateDTO):
    logger.info("Creating a new event")
    # Placeholder for creating an event
    return {"id": 1, **event.dict()}

@app.post("/events/{event_id}/register")
async def register_event(event_id: int, registration: RegisterDTO):
    try:
        logger.info(f"Registering to event {event_id}")
        attendee_add = await Attendees().register(event_id, registration)
        return {"message": f"Registered to event {event_id}", "registration": registration}
    except ValueError as e:
        logger.error(f"Error registering to event {event_id}: {str(e)}")
        return responses.JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except HTTPException as e:
        logger.error(f"HTTP error registering to event {event_id}: {str(e.detail)}")
        return responses.JSONResponse(
            status_code=e.status_code,
            content={"error": e.detail}
        )
    except Exception as e:
        logger.error(f"Unexpected error registering to event {event_id}: {str(e)}")
        return responses.JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred while registering to the event"}
        )
    
@app.get("/events/{event_id}/attendes", response_model=List[AttendeeDTO])
async def get_event_attendees(event_id: int):
    try:
        logger.info(f"Fetching attendees for event {event_id}")
        result = await Attendees().get_attendees(event_id)
        return [AttendeeDTO.from_orm(a) for a in result]
    except Exception as e:
        logger.error(f"Error fetching attendees for event {event_id}: {str(e)}")
        return responses.JSONResponse(
            status_code=500,
            content={"error": "An error occurred while fetching attendees"}
        )