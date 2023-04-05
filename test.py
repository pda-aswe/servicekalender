import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html

#umwandeln in start und stopp der gewünschten zeit
def getEvents(service, count):
    events = None
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=count, singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])
    except:
        pass
    return events

def getEvent(service, eventId):
    event = None
    try:
        event = service.events().get(calendarId="primary", eventId=eventId).execute()
    except:
        pass
    return event


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

def deleteEvent(service,eventId):
    returnStatus = True
    try:
        service.events().delete(calendarId="primary", eventId=eventId).execute()
    except:
        returnStatus = False
    return returnStatus

def updateEvent(service, eventId, eventDetails):
    event = None
    try:
        event = service.events().patch(calendarId='primary',
                                           eventId=eventId, body=eventDetails).execute()
    except:
        pass
    return event

SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/calendar']

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)


#events durchgehen
for event in getEvents(service, 10):
    print(event['status'])
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    print(event['id'], start, end, event['summary'])

#uhrzeit
#d = datetime.now().date()
#tomorrow = datetime(d.year, d.month, d.day, 10)+datetime.timedelta(days=1)
#start = tomorrow.isoformat()
#end = (tomorrow + datetime.timedelta(hours=1)).isoformat()