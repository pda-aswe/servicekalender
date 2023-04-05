import paho.mqtt.client as mqtt
import os
import datetime
import gcalendar
import json

class Messenger:
    def __init__(self):
        self.connected = False
        self.calendarClient = gcalendar.GCalendar()

        #aufbau der MQTT-Verbindung
        self.mqttConnection = mqtt.Client()
        self.mqttConnection.on_connect = self.__onMQTTconnect
        self.mqttConnection.on_message = self.__onMQTTMessage

        #Definition einer Callback-Funktion für ein spezielles Topic
        self.mqttConnection.message_callback_add("req/appointment/next", self.__mailMQTTNextcallback)
        self.mqttConnection.message_callback_add("appointment/create", self.__mailMQTTCreatecallback)
        self.mqttConnection.message_callback_add("appointment/delete", self.__mailMQTTDeletecallback)
        self.mqttConnection.message_callback_add("appointment/update", self.__mailMQTTUpdatecallback)
        self.mqttConnection.message_callback_add("req/appointment/range", self.__mailMQTTRangecallback)

    def connect(self):
        if not self.connected:
            try:
                docker_container = os.environ.get('DOCKER_CONTAINER', False)
                if docker_container:
                    mqtt_address = "broker"
                else:
                    mqtt_address = "localhost"
                self.mqttConnection.connect(mqtt_address,1883,60)
            except:
                return False
        self.connected = True
        return True
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            self.mqttConnection.disconnect()
        return True

    def __onMQTTconnect(self,client,userdata,flags, rc):
        client.subscribe([("req/appointment/next",0),("appointment/create",0),("appointment/delete",0),("appointment/update",0),("req/appointment/range",0)])

    def foreverLoop(self):
        self.mqttConnection.loop_forever()

    def __onMQTTMessage(self,client, userdata, msg):
        pass

    def __mailMQTTNextcallback(self,client, userdata, msg):
        eventData = self.calendarClient.nextEvent()
        if eventData:
            self.mqttConnection.publish("appointment/next",json.dumps(eventData))

    def __mailMQTTCreatecallback(self,client, userdata, msg):
        pass

    def __mailMQTTDeletecallback(self,client, userdata, msg):
        try:
            deleteData = json.loads(str(msg.payload.decode("utf-8")))
        except:
            print("Can't decode message")
            return
        
        reqKeys = ['id']

        if not all(key in deleteData for key in reqKeys):
            print("not all keys available")
            return
        
        self.calendarClient.deleteEvent(deleteData["id"])


    def __mailMQTTUpdatecallback(self,client, userdata, msg):
        pass

    def __mailMQTTRangecallback(self,client, userdata, msg):
        try:
            rangeData = json.loads(str(msg.payload.decode("utf-8")))
        except:
            print("Can't decode message")
            return
        
        reqKeys = ['start','end']

        if not all(key in rangeData for key in reqKeys):
            print("not all keys available")
            return
        
        try:
            datetime.datetime.strptime(rangeData['start'], '%Y-%m-%dT%H:%M:%S%z')
            datetime.datetime.strptime(rangeData['end'], '%Y-%m-%dT%H:%M:%S%z')
        except:
            print("wrong time format")
            return
        
        events = self.calendarClient.rangeEvents(rangeData['start'],rangeData['end'])

        eventsData = {"start":rangeData['start'],"end":rangeData['end'],"events":events}
        self.mqttConnection.publish("appointment/range",json.dumps(eventsData))
        


        
        