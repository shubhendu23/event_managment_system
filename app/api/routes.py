from fastapi import FastAPI, responses, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from config.logger import Logger
from dto.dto import EventDTO, EventCreateDTO, RegisterDTO, AttendeeDTO
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
    '''
    Fetches all events.
    Returns:
        List[EventDTO]: A list of all events.'''
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
    '''Creates a new event.
        Args:
            event (EventCreateDTO): The details of the event to be created.
    '''
    try:
        logger.info("Creating a new event")
        new_event = await Events().create_event(event)
        return EventDTO.from_orm(new_event)
    except Exception as e:
        logger.error(f"Error creating event: {str(e)}")
        return responses.JSONResponse(
            status_code=500,
            content={"error": "An error occurred while creating the event"}
        )

@app.post("/events/{event_id}/register")
async def register_event(event_id: int, registration: RegisterDTO):
    '''Registers an attendee for a specific event.
        Args:
            event_id (int): The ID of the event to register for.
            registration (RegisterDTO): The registration details of the attendee.
    '''
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
async def get_event_attendees(event_id: int, limit:int = Query(10, ge=1),offset:int = Query(0, ge=0)):
    '''Fetches attendees for a specific event with pagination.
        Args:
            event_id (int): The ID of the event to fetch attendees for.
            limit (int): The maximum number of attendees to return (default is 10).
            offset (int): The number of attendees to skip before starting to collect the result set (default is 0).
    '''
    try:
        logger.info(f"Fetching attendees for event {event_id}")
        result = await Attendees().get_attendees(event_id, limit=limit, offset=offset)
        return [AttendeeDTO.from_orm(a) for a in result]
    except Exception as e:
        logger.error(f"Error fetching attendees for event {event_id}: {str(e)}")
        return responses.JSONResponse(
            status_code=500,
            content={"error": "An error occurred while fetching attendees"}
        )