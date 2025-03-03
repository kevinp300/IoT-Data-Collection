import paho.mqtt.client as mqtt
import Adafruit_DHT
import RPi.GPIO as GPIO
import json
import time
import ssl

# AWS IoT Core Configuration
AWS_IOT_ENDPOINT = ""
CERTIFICATE_PATH = "certs/device-certificate.pem.crt"
PRIVATE_KEY_PATH = "certs/private-key.pem.key"
ROOT_CA_PATH = "certs/root-ca.pem"
MQTT_TOPIC = "raspberrypi4/sensors"

# Sensor Configuration
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
PIR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# MQTT Setup
client = mqtt.Client()
client.tls_set(ROOT_CA_PATH, CERTIFICATE_PATH, PRIVATE_KEY_PATH, ssl.CERT_REQUIRED)

client.connect(AWS_IOT_ENDPOINT, 8883, 60)

def read_sensors():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    motion_detected = GPIO.input(PIR_PIN)
    
    if humidity is not None and temperature is not None:
        return {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "motion": bool(motion_detected),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        return None

while True:
    data = read_sensors()
    if data:
        payload = json.dumps(data)
        client.publish(MQTT_TOPIC, payload)
        print(f"Published: {payload}")
    time.sleep(5)
