from src import gcalendar
from unittest.mock import patch

#HIER GLAUB ICH KEINE GUTE MÖGLICHKEIT ZU TESTEN

def test_nextEvent():
    obj = gcalendar.GCalendar()

    #hier kommt immer {} zurück, da man nur events mocken kann, man aber die gwünschten returndaten nicht herstellen kann und deswegen immer im try, except landet
    with patch.object(obj.service, 'events') as mockEvents:
        assert obj.nextEvent() == {}