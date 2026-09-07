import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
TOPIC = "iot/lab/sensor"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
        print(f"Subscribed to: {TOPIC}\n")
    else:
        print(f"Connection failed: {rc}")

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to {BROKER}...")
client.connect(BROKER, 1883, 60)
client.loop_forever()