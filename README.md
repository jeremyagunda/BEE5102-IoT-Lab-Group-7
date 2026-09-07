# BEE 5102 IoT Lab — Temperature & Humidity Monitor

## Group Members
- Jeremy Agunda — 150870
- Husna Hasan — 138040
- Will Iha — 151727
- Alvin Wade — 151955

## Course
BEE 5102: Embedded Systems & IoT  
Strathmore University | July–October 2026

## Project Description
A complete IoT pipeline that reads temperature and humidity from a DHT22 sensor using an ESP32 microcontroller, transmits the data over WiFi via MQTT, and persists it to an SQLite database on a PC.

## Architecture
[DHT22 Sensor] → [ESP32 + MicroPython] → [WiFi + MQTT] → [HiveMQ Broker] → [Python Subscriber] → [SQLite Database]

## Hardware Used
- ESP32-DevKitC development board
- DHT22 (AM2302) temperature/humidity sensor
- 10kΩ pull-up resistor
- Breadboard and jumper wires

## Software Used
- MicroPython v1.29.0 (ESP32_GENERIC)
- Thonny IDE
- Python 3.14 + paho-mqtt
- SQLite (built-in with Python)
- HiveMQ public broker (broker.hivemq.com)

## Files
| File | Description |
|------|-------------|
| `main.py` | MicroPython code for ESP32 — reads DHT22, connects to WiFi, publishes JSON to MQTT |
| `subscriber_db.py` | Python script — subscribes to MQTT, parses JSON, saves to SQLite database |
| `mqtt_listener.py` | Python script — simple MQTT subscriber for verifying messages |
| `BEE5102_IoT_Lab_Report.pdf` | Full lab report with screenshots and documentation |

## Wiring
| DHT22 Pin | ESP32 Pin |
|-----------|-----------|
| VCC | 3.3V |
| Data | GPIO4 (with 10kΩ pull-up to 3.3V) |
| GND | GND |

## How It Works
1. The ESP32 boots and runs `main.py` automatically
2. It connects to WiFi and the HiveMQ MQTT broker
3. Every 5 seconds, it reads the DHT22 sensor and publishes JSON data to `iot/lab/sensor`
4. `subscriber_db.py` on the PC listens to the same topic and inserts data into `sensor_data.db`
5. A `SELECT *` query confirms 12+ rows were stored with timestamps

## Key Results
- ✅ ESP32 successfully flashed with MicroPython firmware
- ✅ DHT22 readings stable: 24.4–25.0°C, 49–50% humidity
- ✅ 12+ JSON messages published and received via MQTT
- ✅ SQLite database confirmed with timestamped rows

## Challenges Overcome
- `esptool.py` not recognized → used `python -m esptool`
- Wrong firmware (ESP8266) → re-downloaded correct ESP32_GENERIC firmware
- `mosquitto_sub` not available → built Python MQTT listener with paho-mqtt
- DHT22 returning None → added missing 10kΩ pull-up resistor
- File path errors → used full paths like `C:\Users\User\Desktop\...`

## Deliverables
1. ✅ Source code (`main.py`, `subscriber_db.py`, `mqtt_listener.py`)
2. ✅ Wiring diagram / breadboard photo
3. ✅ Screenshot: REPL output with live sensor readings
4. ✅ Screenshot: 10+ JSON messages received via MQTT
5. ✅ Screenshot: SQLite SELECT query with timestamps
6. ✅ Lab report (max 5 pages + appendices)
7. ✅ Group work evidence

## Instructor
- Dr. Sitotia (sitotia@strathmore.edu)
- Lab Technologist: jntonjira@strathmore.edu
