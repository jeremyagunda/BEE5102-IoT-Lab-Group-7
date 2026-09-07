import machine
import dht
import network
import time
from umqtt.simple import MQTTClient
import json

WIFI_SSID = "Wifi"
WIFI_PASSWORD = "you12345"
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = b"iot/lab/sensor"

sensor = dht.DHT22(machine.Pin(4))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("WiFi connected:", wlan.ifconfig()[0])
    return wlan

def read_sensor():
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        return temp, hum
    except Exception as e:
        print("Sensor read error:", e)
        return None, None

def publish_data(client, temp, hum):
    payload = json.dumps({
        "temperature": temp,
        "humidity": hum,
        "device": "esp32_lab_group"
    })
    client.publish(MQTT_TOPIC, payload)
    print("Published:", payload)

def main():
    connect_wifi()
    client = MQTTClient("esp32_client", MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT broker")
    msg_count = 0
    while True:
        temp, hum = read_sensor()
        if temp is not None and hum is not None:
            publish_data(client, temp, hum)
            msg_count += 1
            print(f"Message #{msg_count} sent")
        else:
            print("Failed to read sensor, retrying...")
        time.sleep(5)

if __name__ == "__main__":
    main()