#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600); // USB Serial communication rate
  SPI.begin();
  rfid.PCD_Init();
}

void loop() {
  // Look for new cards
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Convert Card UID to String
  String cardID = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (rfid.uid.uidByte[i] < 0x10) cardID += "0";
    cardID += String(rfid.uid.uidByte[i], HEX);
  }
  cardID.toUpperCase();

  // Send UID over USB Serial
  Serial.println(cardID);

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  delay(2000); // Debounce delay
}