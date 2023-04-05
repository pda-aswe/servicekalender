import os
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GCalendar:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            print("Missing Google login credentials")
            quit()
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
        except:
            print("gmail error")
            quit()

    def nextEvent(self):
        nextEvent = {}
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = self.service.events().list(calendarId='primary', timeMin=now,maxResults=1,orderBy='startTime',singleEvents=True).execute()
        except:
            return {}
        
        events = events_result.get('items', [])
        if len(events) > 0:
            nextEvent['start'] = events[0]['start']['dateTime']
            nextEvent['end'] = events[0]['end']['dateTime']
            nextEvent['id'] = events[0]['id']
            nextEvent['summary'] = events[0].get('summary', '')
            nextEvent['location'] = events[0].get('location', '')
            nextEvent['status'] = events[0].get('status', '')
        return nextEvent
    
    def deleteEvent(self,eventID):
        returnStatus = True
        try:
            self.service.events().delete(calendarId="primary", eventId=eventID).execute()
        except:
            returnStatus = False
        return returnStatus
    
    def rangeEvents(self,start,end):

        try:
            startT = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
            endT = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
            if endT < startT:
                print("invalid data")
                return []
        except:
            print("wrong time format")
            return []

        eventsList = []
        try:
            events_result = self.service.events().list(calendarId='primary', timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])
        except:
            return []
        
        for event in events:
            eventData = {}
            eventData['start'] = event['start']['dateTime']
            eventData['end'] = event['end']['dateTime']
            eventData['id'] = event['id']
            eventData['summary'] = event.get('summary', '')
            eventData['location'] = event.get('location', '')
            eventData['status'] = event.get('status', '')
            eventsList.append(eventData)

        return eventsList
    
    def createEvent(self,start,end,summary,location):
        eventData = {
            "summary": summary,
            "location": "",
            "description": "",
            "start": {
                "dateTime": start,
                "timeZone": "Europe/Berlin"
            },
            "end": {
                "dateTime": end,
                "timeZone": "Europe/Berlin"
            }
        }

        try:
            startT = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
            endT = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
            if endT < startT:
                print("invalid data")
                return -1
        except:
            print("wrong time format")
            return -1

        if location != None:
            eventData["location"] = location

        try:
            event = self.service.events().insert(calendarId='primary', body=eventData).execute()
        except:
            return -1
        return event['id']
    
    def updateEvent(self,data):
        if "id" not in data:
            return None

        eventData = {}
        if "start" in data:
            eventData["start"] = {
                "dateTime": data['start'],
                "timeZone": "Europe/Berlin"
            }
        
        if "end" in data:
            eventData["end"] = {
                "dateTime": data['end'],
                "timeZone": "Europe/Berlin"
            }
        
        if 'location' in data:
            eventData['location'] = data['location']

        if 'summary' in data:
            eventData['summary'] = data['summary']

        try:
            event = self.service.events().patch(calendarId='primary', eventId=data['id'], body=eventData).execute()
        except:
            return None
        return event