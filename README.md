# AWS Cloud-Integrated RFID Attendance System

An end-to-end **IoT-based RFID Attendance Monitoring System** that records RFID card scans and securely uploads attendance data to **Amazon DynamoDB** through **AWS IoT Core** using **MQTT over TLS**.

This project demonstrates the integration of **Embedded Systems**, **Python**, and **AWS Cloud Services** to build a secure, real-time attendance management solution.

---

# 📌 Features

- 📡 Reads RFID card UID using the MFRC522 module
- 🔌 Sends RFID data from Arduino to Python via Serial USB
- ☁️ Publishes attendance records to AWS IoT Core using MQTT over TLS
- 🗄 Automatically stores attendance records in Amazon DynamoDB
- 🔒 Uses Mutual TLS (mTLS) with X.509 certificates for secure communication
- ⚡ Real-time cloud-based attendance logging
- 📈 Easily scalable for schools, colleges, offices, and industries

---

# 🏗 System Architecture

```text
           RFID Card / Tag
                 │
                 ▼
      MFRC522 RFID Reader Module
                 │
            SPI Communication
                 │
                 ▼
            Arduino Uno
                 │
         USB Serial Communication
                 │
                 ▼
      Python Edge Gateway
   (pyserial + paho-mqtt)
                 │
        MQTT over TLS (8883)
                 │
                 ▼
          AWS IoT Core
                 │
          AWS IoT SQL Rule
                 │
                 ▼
      Amazon DynamoDB
       (AttendanceLogs)
```

---

# 🛠 Tech Stack

## Hardware

- Arduino Uno
- MFRC522 RFID Reader (13.56 MHz)
- RFID Tags/Cards
- USB Cable

## Software

- Arduino IDE
- Python 3.x

## Python Libraries

- paho-mqtt
- pyserial

## AWS Services

- AWS IoT Core
- Amazon DynamoDB
- AWS IAM
- AWS IoT SQL Rules

---

# 🔗 Communication Protocols

| Layer | Technology |
|--------|------------|
| RFID Reader → Arduino | SPI |
| Arduino → Python | USB Serial |
| Python → AWS IoT Core | MQTT over TLS |
| AWS IoT Rule → DynamoDB | AWS IoT SQL Rule |

---

# 🔒 Security

This project follows AWS security best practices.

- Mutual TLS (mTLS)
- X.509 Device Certificates
- Private Device Keys
- Amazon Root CA
- AWS IoT Policies
- Secure MQTT Communication (TLS 1.2/1.3)

Sensitive files are excluded using `.gitignore`.

---

# 📁 Repository Structure

```text
AWS-Cloud-Integrated-RFID-Attendance-System/
│
├── RFID_Reader.ino/
│   └── RFID_Reader.ino.ino
│
├── AWS_Bridge_IOT.py
│
├── .gitignore
│
└── README.md
```

---

# ⚙ Hardware Connections

Connect the MFRC522 RFID Reader to the Arduino Uno as shown below.

| MFRC522 Pin | Arduino Uno Pin |
|-------------|-----------------|
| SDA (SS) | D10 |
| SCK | D13 |
| MOSI | D11 |
| MISO | D12 |
| RST | D9 |
| 3.3V | 3.3V |
| GND | GND |

> **Important:** Never connect the MFRC522 module to the Arduino 5V pin.

---

# 🚀 Setup Guide

## Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/AWS-Cloud-Integrated-RFID-Attendance-System.git

cd AWS-Cloud-Integrated-RFID-Attendance-System
```

---

## Step 2 — Install Arduino Libraries

Open **Arduino IDE**

Install:

- MFRC522 Library
- SPI Library (already included)

---

## Step 3 — Upload Arduino Firmware

Open

```
RFID_Reader.ino/RFID_Reader.ino.ino
```

Select

- Board → Arduino Uno
- Correct COM Port

Upload the sketch.

---

## Step 4 — Create AWS Resources

Create the following AWS resources.

### AWS IoT Core

Create an IoT Thing

Example:

```
Arduino_RFID_Scanner
```

Download

- Device Certificate
- Private Key
- Amazon Root CA 1

Attach an IoT Policy with permissions:

- iot:Connect
- iot:Publish

---

### Amazon DynamoDB

Create a table

```
AttendanceLogs
```

---

### AWS IoT Rule

Create an SQL Rule

Example Topic

```
attendance/scan
```

Configure the rule to insert incoming messages into the DynamoDB table.

---

## Step 5 — Install Python Dependencies

```bash
pip install paho-mqtt pyserial
```

---

## Step 6 — Configure Python Bridge

Place the following files beside

```
AWS_Bridge_IOT.py
```

- AmazonRootCA1.pem
- Device Certificate
- Private Key

Update the configuration.

```python
COM_PORT = "COM3"

AWS_ENDPOINT = "xxxxxxxxxxxxx.iot.us-east-1.amazonaws.com"

PATH_TO_CERT = "device.pem.crt"

PATH_TO_KEY = "private.pem.key"

PATH_TO_ROOT_CA = "AmazonRootCA1.pem"
```

---

## Step 7 — Run the Python Gateway

```bash
python AWS_Bridge_IOT.py
```

The gateway continuously:

- Reads RFID UID from Arduino
- Creates JSON payload
- Publishes to AWS IoT Core
- Stores attendance in DynamoDB

---

# 📤 Sample MQTT Payload

```json
{
  "CardID": "A1B2C3D4",
  "Timestamp": "2026-07-24T12:00:00Z"
}
```

---

# 🗄 DynamoDB Record Example

| CardID | Timestamp |
|----------|-----------------------|
| A1B2C3D4 | 2026-07-24T12:00:00Z |

---

# 🔄 Project Workflow

```text
RFID Card
      │
      ▼
MFRC522 Reader
      │
      ▼
Arduino Uno
      │
Serial USB
      │
      ▼
Python Gateway
      │
MQTT over TLS
      │
      ▼
AWS IoT Core
      │
IoT SQL Rule
      │
      ▼
Amazon DynamoDB
```

---

# 📚 Learning Outcomes

This project demonstrates practical experience in:

- Embedded Systems
- Arduino Programming
- RFID Technology
- Python Programming
- Serial Communication
- MQTT Protocol
- AWS IoT Core
- Amazon DynamoDB
- AWS IAM
- IoT Security
- Cloud Integration
- Real-Time Data Streaming

---

# 📌 Future Improvements

- Web Dashboard for Attendance
- Student Database Integration
- Email Notifications
- SMS Alerts
- Attendance Analytics
- AWS Lambda Integration
- Amazon SNS Notifications
- CloudWatch Monitoring
- Mobile Application
- QR + RFID Hybrid Authentication

---

# 🔒 Security Notice

For security reasons, the following files are **NOT** included in this repository.

```text
*.pem
*.crt
*.key
AmazonRootCA1.pem
AWS Certificates
AWS Endpoint Credentials
```

These files are ignored using `.gitignore`.

---

# 📄 License

This project is intended for educational and learning purposes.

Feel free to fork, modify, and enhance it for your own projects.

---

# 👨‍💻 Author

**Dhikshith**

**B.E. Electronics and Communication Engineering**

Rajalakshmi Institute of Technology

**Skills**

- Embedded Systems
- IoT
- AWS Cloud
- Python
- Arduino
- MQTT
- RFID
- DynamoDB

---
