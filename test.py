import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html

eventTemplate = {
  "summary": "Title",
  "location": "",
  "description": "",
  "start": {
    "dateTime": "2023-04-04T22:00:00",
    "timeZone": "Europe/Berlin"
  },
  "end": {
    "dateTime": "2023-04-04T22:04:00",
    "timeZone": "Europe/Berlin"
  }
}

def createEvent(service, eventDetails):
    returnId = None
    try:
        event = service.events().insert(calendarId='primary', body=eventDetails).execute()
        returnId = event[id]
    except:
        pass
    return returnId

def updateEvent(service, eventId, eventDetails):
    event = None
    try:
        event = service.events().patch(calendarId='primary',
                                           eventId=eventId, body=eventDetails).execute()
    except:
        pass
    return event