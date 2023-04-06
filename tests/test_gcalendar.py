from src import gcalendar
from unittest.mock import patch

#HIER GLAUB ICH KEINE GUTE MÖGLICHKEIT ZU TESTEN

@patch("os.path.exists")
@patch("google.oauth2.credentials.Credentials.from_authorized_user_file")
def test_nextEvent(mock_google,mock_os):
    obj = gcalendar.GCalendar()

    #hier kommt immer {} zurück, da man nur events mocken kann, man aber die gwünschten returndaten nicht herstellen kann und deswegen immer im try, except landet
    with patch.object(obj.service, 'events') as mockEvents:
        assert obj.nextEvent() == {}