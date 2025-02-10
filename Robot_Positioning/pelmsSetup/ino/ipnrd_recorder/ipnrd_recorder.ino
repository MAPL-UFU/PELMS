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
#include <LiquidCrystal.h>
#include <HardwareSerial.h>
#include <Pn532NfcReader.h>

/* FUNCTION TO SET THE TEXT TO PRINT */
#define LCD_print(pos, msg, length, type, time) ({\
  char text[length + 1];\
  char padding[LCD_WIDTH + 1];\
  String setup = type;\
  \
  for(int i = 0; i <= LCD_WIDTH; i++) padding[i] = i != LCD_WIDTH ? ' ':'\0';\
  setup.toLowerCase();\
  \
  if (setup == "left") snprintf(text, length + 1, "%s%s", msg, padding);\
  else {\
    int space = length - strlen(msg);\
    if (setup == "center") {\
      space = space - space%2 == 1 ? 1:0;\
      snprintf(text, length + 1, "%*.*s%s%s", space/2, space/2, padding, msg, padding);\
    }\
    if (setup == "right") snprintf(text, length + 1, "%*.*s%s", space, space, padding, msg);\
  }\
  \
  lcd.setCursor(0, pos);\
  lcd.print(text);\
  delay(time);\
})

/* DEFINING MACROS FOR THE SIZE AND THE PINS OF LIQUIDCRYSTAL LCD */
#define LCD_WIDTH 16
#define LCD_HEIGHT 2
#define RS 26
#define Enable 27
#define D4 15
#define D5 2
#define D6 4
#define D7 5

/* DECLARATION OF OBJECT FOR MQTT COMUNICATION AND LCD DISPLAYING */
WiFiClient espClient;
PubSubClient MQTT(espClient);
LiquidCrystal lcd(RS, Enable, D4, D5, D6, D7);
TaskHandle_t Task1;

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

String status = "", topic_status = "";
int sizearray[] = {1, 2};
volatile bool start[] = {false, false};

/** Input of Fire Vector:
 * The Fire Vector must contain the number of transitions in the PetriNet
*/
uint16_t* mFireVector = new uint16_t[1]{1};

void setup(void) {
  Serial.begin(115200);
  lcd.begin(LCD_WIDTH, LCD_HEIGHT);

  LCD_print(0, "Starting System", LCD_WIDTH, "left", 2000);
  LCD_print(0, "iPNRD Recorder", LCD_WIDTH, "center", 0);
  LCD_print(1, "Connecting...", LCD_WIDTH, "left", 700);

  /** START THE CONNECTION TO WIFI
   * This call start the method connection that try to connect to SSID WiFi. If WiFi is not connected try another SSID.
   * Commands:
   *   setWiFi(const char* ssid, const char* password)
   *   setWiFi(const char* ssid, wpa2_auth_method_t method, const char* identity, const char* username, const char* password)
   *   connect()
   *   status()
  */
  do {
    username == "XXXX" ? ewifi.setWiFi(SSID, password):ewifi.setWiFi(SSID, WPA2_AUTH_PEAP, anonymous, username, password);
    ewifi.connect();

    if(ewifi.status() != WL_CONNECTED) printf("\nConnection failed (%s)...\n", SSID);
    else break;
  } while(true);

  LCD_print(1, "Connected!", LCD_WIDTH, "left", 1000);
  LCD_print(0, "Setup iPNRD Tag", LCD_WIDTH, "center", 0);
  LCD_print(1, "", LCD_WIDTH, "left", 700);

  // Setup of Server and Subscribe
  MQTT.setServer(MQTTServer, MQTTPort);
  MQTT.setCallback(callback);

  // Setup a Task using the free core of ESP32
  int CORE_ID = int(!xPortGetCoreID());
  xTaskCreatePinnedToCore(
    Task1code, // Task function
    "Task1",   // Name of the Task to atach
    10000,     // Size to alocated to Task (Word or Byte)
    NULL,      // Task argument to be passed (void*)
    0,         // Priority of the Task [0 a 25]
    &Task1,    // Task ID
    CORE_ID);  // Task core ID (0 ou 1)
  delay(500);
}

/* TASK FUNCTION USING FREE CORE OF ESP32 */
void Task1code(void* pvParameters) {
  Serial.print("Conexões MQTT rodando no nucleo ");
  Serial.println(xPortGetCoreID());

  for (;;) {
    if (!MQTT.connected()) conectarMQTT();

    MQTT.loop();
  }
}

/* LOOP FUNCTION TO RUNNING PROGRAM */
void loop() { }

/* CALLBACK FUNCTION FOR SUBSCRIBE TOPICS */
void callback(char* topic, byte* payload, unsigned int length) {
  String msg = "";
  String msg_topic = "";

  for(int i = 0; i < strlen(topic); i++) msg_topic += (char)topic[i];
  for(int i = 0; i < length; i++) msg += (char)payload[i];

  printf("Tópico: %s\tMensagem: %s\n", msg_topic.c_str(), msg.c_str());

  if (status != msg || topic_status != msg_topic) {
    status = msg;
    topic_status = msg_topic;
    msg.toLowerCase();
    if (!strcmp(msg_topic.c_str(), "PELMS-MQTT/len_place")) {
      sizearray[0] = msg.toInt();
      start[0] = true;
    } else if (!strcmp(msg_topic.c_str(), "PELMS-MQTT/len_transition")) {
      sizearray[1] = msg.toInt();
      start[1] = true;
    } else if (!strcmp(msg_topic.c_str(), "PELMS-MQTT/fire_vector") && start[0] && start[1]) {
      resize(mFireVector, sizearray[1], msg);

      // printf("Places: %d\nTransition: %d\nFire Position: {", sizearray[0], sizearray[1]);
      // for (int i = 0; i < sizearray[1]; i++)
        // i == (sizearray[1] - 1) ? printf("%d}\n", mFireVector[i]):printf("%d, ", mFireVector[i]);
      LCD_print(1, "Starting", LCD_WIDTH, "left", 700);

      // Preparing the tag information
      eraseRFID();
      cleanRFID();
      formatRFID();
      recordRFID();
      for (int i = 0; i < 2; i++)
        start[i] = false;
    }
  }
}

void eraseRFID() {
  #if 0
    PN532 tag(pn532spi);
  #elif 1
    PN532 tag(pn532hsu);
  #else
    PN532 tag(pn532_i2c);
  #endif

  nfc.begin();
  tag.begin();

  // Set the max number of retry attempts to read from a card
  // This prevents us from waiting forever for a card, which is
  // the default behaviour of the PN532.
  tag.setPassiveActivationRetries(0xFF);

  // configure board to read RFID tags
  tag.SAMConfig();

  uint8_t uid[] = {0, 0, 0, 0, 0, 0, 0};
  uint8_t uidLength;
  String tagID = "";

  LCD_print(1, "Place the Tag!!!", LCD_WIDTH, "left", 700);

  // Identifier if tag is present
  while (!nfc.tagPresent()) delay(100);
  LCD_print(1, "Tag Presented!!!", LCD_WIDTH, "left", 700);
  
  tag.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
  for(int i = 0; i < uidLength; i++) tagID += String(uid[i], HEX);
  tagID.toUpperCase();
  char text_to_print[20];
  snprintf(text_to_print, 20, "TagID: %s", tagID);
  LCD_print(1, text_to_print, LCD_WIDTH, "left", 2000);

  // Erase the tag returning the success of erasing
  LCD_print(1, "Erasing the Tag.", LCD_WIDTH, "left", 700);
  
  bool success = nfc.erase();

  // Return the message of erasing
  LCD_print(1, success ? "Success":"Tag Erased!", LCD_WIDTH, "left", 700);
}

void cleanRFID() {
  nfc.begin();

  // Identifier if tag is present
  while (!nfc.tagPresent()) delay(500);

  // Return the tag do Factory and returning the success of Factory Setup
  LCD_print(1, "Factory Setup", LCD_WIDTH, "left", 700);
  
  bool success = nfc.clean();

  LCD_print(1, success ? "Success":"Setup had done.", LCD_WIDTH, "left", 700);
}

void formatRFID() {
  nfc.begin();

  // Identifier if tag is present
  while (!nfc.tagPresent()) delay(500);

  // Format the tag returning the success of formating
  LCD_print(1, "Format the Tag", LCD_WIDTH, "left", 700);
  
  bool success = nfc.format();

  LCD_print(1, success ? "Success":"Tag formated!", LCD_WIDTH, "left", 700);
}

/* Not Used */
void readRFID() {
  // Read the information of the Tag
  NfcTag tag = nfc.read();

  // Print the information of the Tag
  tag.print();
}

void recordRFID() {
  /** Creation of the reader and PNRD objects
   * Pnrd(readerPointer, num_places, num_transitions, num_max_of_inputs, num_max_of_outputs, hasConditions, hasTagHistory)
  */
  Pnrd pnrd = Pnrd(reader, sizearray[0], sizearray[1]); //leitor, no estados e no transicoes

  // Initializing PN532reader
  reader->initialize();

  //Defining the Fire Vector to be recorded
  pnrd.setFireVector(mFireVector);

  //Setting of the classic iPNRD approach
  pnrd.setAsTagInformation(PetriNetInformation::FIRE_VECTOR);
  pnrd.setAsTagInformation(PetriNetInformation::TAG_HISTORY);
  LCD_print(1, "Storing in Tag!", LCD_WIDTH, "left", 700);

  // Identifier if tag is present
  while (!nfc.tagPresent()) delay(500);

  bool success = pnrd.saveData() == WriteError::NO_ERROR;

  // Cormfirming if data is saved
  LCD_print(1, success ? "iPNRD Stored!":"Error of Storing", LCD_WIDTH, "left", 2000);

  LCD_print(1, "", LCD_WIDTH, "left", 0);
}

/* MQTT FUNCTION FOR CONECT TO SERVER */
void conectarMQTT() {
  // printf("%s\n", MQTTClientid);
  while (!MQTT.connected())
    if (MQTT.connect(MQTTClientid)) MQTT.subscribe(topic);
}

/* RESIZE THE MATRIX */
void resize(uint16_t *&original, int setSIZE, String msg) {
	uint16_t *temporiginal = new uint16_t[setSIZE];
  int j = 0;

	for (int i = 0; i < msg.length(); i++) {
    String text = String(msg.charAt(i));
    if (strcmp(text.c_str(), "{") && strcmp(text.c_str(), ",") && strcmp(text.c_str(), " ") && strcmp(text.c_str(), "}")) {
		  temporiginal[j] = text.toInt();
      j++;
    }
  }

	delete[] original;
	original = temporiginal; //point old array to new array
}