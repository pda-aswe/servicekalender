import os
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