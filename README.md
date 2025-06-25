# event_management_system

This is a FastApi Based Backend service for event managememt
Common functionality Supported are:

POST Method
    *) Create event
    *) Register attenedees

GET Method
    *) Get Attendees
    *) Get Events

There are some contraints and limitation defined such as:
    *) max_capacity should not exceed
    *) valid Email
    *) Unique qmail oer registration for an event.

# Folder Structure
app
    api -> router Holding all api endpoitns
    config -> Storeing DB config and logger configs
    dto -> holding dto's for all api request and response
    models-> data models for sqlalchemy orm
    service -> Base logics for operation on event and attendees tables.
    test -> testcases for all apis
data -> Holding .sqlite file as sample data with table creation 

# Steps to run
Switch to the app directory
Install dependencies: RUN pip install -r requirments.in
Set up the database:: RUN sqlite3 ../data/event_managment.sqlite < schemas.sql
App Run: RUN python3 uvicorn app.main:app --reload


# Sample Ussage
GET Events
curl --location --request GET '127.0.0.1:8000/events/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "attendee_name": "Stev",
    "attendee_email": "abc@gmail.com",
    "contact_number": "12345789"
}'

POST events
curl --location '127.0.0.1:8000/events/' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Testing EMS",
    "start_datetime": "2025-07-01T00:00:00",
    "end_datetime": "2025-07-10T00:00:00",
    "max_capacity": 2,
    "location": "Hyderabad",
    "description": "A test event"
}'

POST REGISTREE
curl --location '127.0.0.1:8000/events/2/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "attendee_name": "Stev",
    "attendee_email": "abc@gmail.com",
    "contact_number": "12345789"
}'

GET Attendees
curl --location --request GET '127.0.0.1:8000/events/2/attendees' \
--header 'Content-Type: application/json' \
--data-raw '{
    "attendee_name": "Stev",
    "attendee_email": "abc@gmail.com",
    "contact_number": "12345789"
}'

