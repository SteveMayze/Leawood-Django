

import paho.mqtt.client as mqtt

client = mqtt.Client()

client.connect("leawood", 1883, 60)

client.publish("leawood/hello", "{'type':'print.test','text':'another message through mqtt'}", qos=0, retain=False)



