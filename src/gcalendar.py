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
        if len(events) >= 0:
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