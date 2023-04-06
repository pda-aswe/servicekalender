from src import messenger
from unittest.mock import patch, ANY, MagicMock
import json

@patch("gcalendar.GCalendar")
def test_connect(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.connect()
        mock_connect.connect.assert_called_with("localhost",1883,60)

@patch("gcalendar.GCalendar")
def test_disconnect(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'connected', True), patch.object(obj, 'mqttConnection') as mock_connect:
        obj.disconnect()
        mock_connect.disconnect.assert_called()

@patch("gcalendar.GCalendar")
def test_foreverLoop(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'mqttConnection') as mock_connect:
        obj.foreverLoop()
        mock_connect.loop_forever.assert_called()

@patch("gcalendar.GCalendar")
def test_onMQTTconnect(mock_travel):
    obj = messenger.Messenger()

    mock_client = MagicMock()

    obj._Messenger__onMQTTconnect(mock_client,None,None,None)

    mock_client.subscribe.assert_called_with([("req/appointment/next",0),("appointment/create",0),("appointment/delete",0),("appointment/update",0),("req/appointment/range",0)])


@patch("gcalendar.GCalendar")
def test_onMQTTMessage(mock_travel):
    obj = messenger.Messenger()

    try:
        obj._Messenger__onMQTTMessage(MagicMock(),None,None)
        assert True
    except:
        assert False

class DummyMSG:
    def __init__(self):
        self.payload = "Test"

    def set_payload(self,data):
        self.payload = str.encode(data)

@patch("gcalendar.GCalendar")
def test_mailMQTTCreatecallback(mock_travel):
    obj = messenger.Messenger()

    responseData = DummyMSG()

    msgData = {
        "start":"2023-04-04T22:00:00+02:00",
        "end":"2023-04-04T22:00:00+02:00",
        "summary":"test"
    }

    responseData.set_payload(json.dumps(msgData))

    with patch.object(obj, 'calendarClient') as mockCalendar:
        obj._Messenger__mailMQTTCreatecallback(None,None,responseData)
        mockCalendar.createEvent.assert_called_with('2023-04-04T22:00:00+02:00', '2023-04-04T22:00:00+02:00', 'test', None)

@patch("gcalendar.GCalendar")
def test_mailMQTTDeletecallback(mock_travel):
    obj = messenger.Messenger()

    responseData = DummyMSG()

    msgData = {
        "id":"asdf"
    }

    responseData.set_payload(json.dumps(msgData))

    with patch.object(obj, 'calendarClient') as mockCalendar:
        obj._Messenger__mailMQTTDeletecallback(None,None,responseData)
        mockCalendar.deleteEvent.assert_called_with("asdf")


@patch("gcalendar.GCalendar")
def test_mailMQTTUpdatecallback(mock_travel):
    obj = messenger.Messenger()

    responseData = DummyMSG()

    msgData = {
        "id":"asdf"
    }

    responseData.set_payload(json.dumps(msgData))

    with patch.object(obj, 'calendarClient') as mockCalendar:
        obj._Messenger__mailMQTTUpdatecallback(None,None,responseData)
        mockCalendar.updateEvent.assert_called_with(msgData)

@patch("gcalendar.GCalendar")
def test_mailMQTTRangecallback(mock_travel):
    obj = messenger.Messenger()

    responseData = DummyMSG()

    msgData = {
        "start":"2023-04-04T22:00:00+02:00",
        "end":"2023-04-04T22:00:00+02:00"
    }

    responseData.set_payload(json.dumps(msgData))

    with patch.object(obj, 'calendarClient') as mockCalendar, patch.object(obj, "mqttConnection") as mockConnection:
        mockCalendar.rangeEvents.return_value = ""

        obj._Messenger__mailMQTTRangecallback(None,None,responseData)

        mockCalendar.rangeEvents.assert_called_with("2023-04-04T22:00:00+02:00","2023-04-04T22:00:00+02:00")
        mockConnection.publish.assert_called_with("appointment/range",json.dumps({"start": "2023-04-04T22:00:00+02:00", "end": "2023-04-04T22:00:00+02:00", "events": ""}))

@patch("gcalendar.GCalendar")
def test_mailMQTTNextcallback(mock_travel):
    obj = messenger.Messenger()

    with patch.object(obj, 'calendarClient') as mockCalendar, patch.object(obj, "mqttConnection") as mockConnection:
        mockCalendar.nextEvent.return_value = {"test":"test"}

        obj._Messenger__mailMQTTNextcallback(None,None,None)

        mockCalendar.nextEvent.assert_called()
        mockConnection.publish.assert_called_with("appointment/next",json.dumps({"test":"test"}))