import time
import json
import serial
import paho.mqtt.client as mqtt

# ==============================================================================
# 1. CONFIGURATION (REPLACE WITH YOUR OWN CREDENTIALS BEFORE RUNNING LOCALLY)
# ==============================================================================

# Serial Port connected to your Arduino Uno
COM_PORT = 'COM3'  # Update to your local port (e.g., 'COM3', 'COM4', '/dev/ttyUSB0')
BAUD_RATE = 9600

# AWS IoT Core Data Endpoint (Found in AWS IoT Console > Settings)
AWS_ENDPOINT = "YOUR_AWS_IOT_ENDPOINT_HERE.iot.us-east-1.amazonaws.com"

# X.509 Certificate File Paths (Place these files in the same directory as this script)
PATH_TO_CERT = "YOUR_CERTIFICATE_FILE.pem.crt"
PATH_TO_KEY = "YOUR_PRIVATE_KEY_FILE.pem.key"
PATH_TO_ROOT_CA = "AmazonRootCA1.pem"

# AWS IoT MQTT Topic
MQTT_TOPIC = "attendance/scan"

# ==============================================================================
# 2. SETUP AWS MQTT CLIENT
# ==============================================================================
print("Connecting to AWS IoT Core...")

try:
    # Supports Paho MQTT v2 API
    mqtt_client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2, 
        client_id="Python_Arduino_Bridge"
    )
except AttributeError:
    # Fallback for older Paho MQTT 1.x versions
    mqtt_client = mqtt.Client(client_id="Python_Arduino_Bridge")

# Configure TLS/SSL Security Certificates
mqtt_client.tls_set(
    ca_certs=PATH_TO_ROOT_CA,
    certfile=PATH_TO_CERT,
    keyfile=PATH_TO_KEY
)

try:
    mqtt_client.connect(AWS_ENDPOINT, 8883, keepalive=60)
    mqtt_client.loop_start()
    print("Successfully connected to AWS IoT Core!")
except Exception as e:
    print(f"Failed to connect to AWS IoT Core: {e}")
    exit(1)

# ==============================================================================
# 3. SETUP SERIAL & READ RFID DATA
# ==============================================================================
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to Arduino on port {COM_PORT}. Ready for RFID scans...\n")
except Exception as e:
    print(f"Could not open Serial Port {COM_PORT}: {e}")
    exit(1)

while True:
    try:
        if ser.in_waiting > 0:
            # Read line from Arduino Serial output
            card_id = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if card_id:
                # Generate ISO 8601 Timestamp
                timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                
                # Construct JSON Payload
                payload = {
                    "CardID": card_id,
                    "Timestamp": timestamp
                }
                
                # Publish payload to AWS IoT Core
                mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
                print(f"[SENT TO AWS] CardID: {card_id} | Timestamp: {timestamp}")
                
    except KeyboardInterrupt:
        print("\nStopping Python Bridge...")
        mqtt_client.loop_stop()
        ser.close()
        break
    except Exception as e:
        print(f"Error reading serial data: {e}")
