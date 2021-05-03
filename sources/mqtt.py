from mqtt import mqtt


class MQTTClient():
    def __init__(self, name):
        self._client = mqtt.Client(name, True)
        self._client.on(mqtt.SUBACK, self._confirm_subscribe)
        self._client.on(mqtt.UNSUBACK, self._confirm_unsubscribe)


    def connect(self, read_func):
        self._client.connect("test.mosquitto.org", keepalive=0)
        self._client.loop(read_func)


    def _confirm_subscribe(self, data):
        print("subscribed")


    def _confirm_unsubscribe(self, data):
        print("unsubscribed")


    def subscribe(self, topic):
        self._client.subscribe([[topic, 0]])


    def publish(self, topic, data="", retain=False):
        self._client.publish("iot/data/" + topic, str(data), retain=retain)
