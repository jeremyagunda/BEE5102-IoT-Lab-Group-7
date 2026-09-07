import paho.mqtt.client as mqtt
import sqlite3
import json
from datetime import datetime
import time

BROKER = "broker.hivemq.com"
TOPIC = "iot/lab/sensor"
DB_NAME = "sensor_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        device TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(temp, hum, device):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO sensor_readings 
        (timestamp, temperature, humidity, device) 
        VALUES (?, ?, ?, ?)''', (timestamp, temp, hum, device))
    conn.commit()
    conn.close()
    print(f"[{timestamp}] Saved: {temp}C, {hum}%")

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
        print(f"Subscribed to: {TOPIC}\n")
    else:
        print(f"Connection failed: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        temp = payload.get("temperature")
        hum = payload.get("humidity")
        device = payload.get("device", "unknown")
        print(f"Received: {payload}")
        save_to_db(temp, hum, device)
    except Exception as e:
        print(f"Error: {e}")

def main():
    init_db()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message
    print(f"Connecting to {BROKER}")
    client.connect(BROKER, 1883, 60)
    client.loop_start()
    print("Collecting data for 60 seconds...")
    try:
        time.sleep(60)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        client.loop_stop()
        client.disconnect()
        print("\n=== DATABASE CONTENTS ===")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sensor_readings ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.close()

if __name__ == "__main__":
    main()