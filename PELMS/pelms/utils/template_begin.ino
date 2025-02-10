/**
 * Created on Dec, 2024
 * @headerfile: PNRD recorder
 * 
 * @details: This code receive message from MQTT protocol and set the variables of
 * the PNRD/iPNRD to be stored in a tag.
 *   1- MQTT set the variables of PNRD/iPNRD
 *   2- When tag presented it erase, restore to factory and format the tag as NDEF format
 *   3- Then it stores the PNRD/iPNRD in the tag using NDEF format
 * 
 * @author: Álisson Carvalho Vasconcelos
 * @authors updater: 
 * @authors github: AlissonCV
 * 
 * @copyright: Free for All
*/

#include <EWiFi.h>
#include <PubSubClient.h>
#include <WiFiPassword.h>
#include <HardwareSerial.h>
#include <Pn532NfcReader.h>

/* DECLARATION OF OBJECT FOR MQTT COMUNICATION AND LCD DISPLAYING */
WiFiClient espClient;
PubSubClient MQTT(espClient);

#if 0
  #include <SPI.h>
  #include <PN532_SPI.h>

  PN532_SPI pn532spi(SPI, port);
  NfcAdapter nfc = NfcAdapter(pn532spi);
#elif 1
  #define NDEF_DEBUG

  #include <PN532_HSU.h>

  //Rotines related with the configuration of the RFID reader PN532
  HardwareSerial sSerial(port);
  // If using ESP32 and Serial2 is not working follow the steps to use hardware serial to solve the problem (https://esp32.com/viewtopic.php?t=4738)
  PN532_HSU pn532hsu(sSerial);
  NfcAdapter nfc(pn532hsu);
#else
  #include <Wire.h>
  #include <PN532_I2C.h>

  PN532_I2C pn532_i2c(Wire);
  NfcAdapter nfc = NfcAdapter(pn532_i2c);
#endif

Pn532NfcReader* reader = new Pn532NfcReader(&nfc);