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

String status = "", topic_status = "";
int sizearray[] = {1, 2};

/** Input of Incidence Matrix
 * The size of Incidence Matrix must contain the number of transitions and the number of places in PetriNet
*/
int8_t* mIncidenceMatrix = new int8_t[2]{-1, 1};

/** Input of Token Vector
 * The size of Token Vector must contain the number of places in PetriNet
*/
uint16_t* mStartingTokenVector = new uint16_t[2]{1, 0};

uint32_t tagId = 0xFFFFFFFF;

void setup(void) {
  Serial.begin(115200);
  delay(1000);

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
    else {break;}
  } while(true);

  printf("Connected to %s!\n", SSID);

  // Setup of Server and Subscribe
  MQTT.setServer(MQTTServer, MQTTPort);
  MQTT.setCallback(callback);
}

/* LOOP FUNCTION TO RUNNING PROGRAM */
void loop() {
  if (!MQTT.connected()) conectarMQTT();

  MQTT.loop();
}

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
    if (!strcmp(msg_topic.c_str(), "PELMS-MQTT/fire/len_place")) {
      sizearray[0] = msg.toInt();
    } else if (!strcmp(msg_topic.c_str(), "PELMS-MQTT/fire/len_transition")) {
      sizearray[1] = msg.toInt();
    } else if (!strcmp(msg_topic.c_str(), "PELMS-MQTT/fire/incidence_matrix")) {
      resize(mIncidenceMatrix, sizearray[0]*sizearray[1], msg);
    } else if (!strcmp(msg_topic.c_str(), "PELMS-MQTT/fire/marking_vector")) {
      resize(mStartingTokenVector, sizearray[0], msg);

      // printf("Places: %d\nTransition: %d\nReader: %s\nIncidence Matrix: {", sizearray[0], sizearray[1], readerID.c_str());
      // for (int i = 0; i < (sizearray[0]*sizearray[1]); i++)
        // i == (sizearray[0]*sizearray[1] - 1) ? printf("%d}\nMarking Vector: {", mIncidenceMatrix[i]):printf("%d, ", mIncidenceMatrix[i]);
      // for (int i = 0; i < sizearray[0]; i++)
        // i == (sizearray[0] - 1) ? printf("%d}\n", mStartingTokenVector[i]):printf("%d, ", mStartingTokenVector[i]);

    }
  }
}

void start_PNRD(){
  printf("Starting Tag Reader!!\n");

  Pnrd pnrd = Pnrd(reader,sizearray[0], sizearray[1], false, true);

  reader->initialize();

  //Setting of the application Petri net approach
  pnrd.setTokenVector(mStartingTokenVector);
  pnrd.setIncidenceMatrix(mIncidenceMatrix);

  //Setting of the classic iPNRD approach
  pnrd.setAsTagInformation(PetriNetInformation::FIRE_VECTOR);
  pnrd.setAsTagInformation(PetriNetInformation::TAG_HISTORY);

  FireError fireError;

  //In case of a successful reading
  while (pnrd.getData() != ReadError::NO_ERROR);

  //Checks if it's a new tag
  if (tagId != pnrd.getTagId()) {
    tagId = pnrd.getTagId();
    Serial.print("\nNew tag. Id code: ");
    Serial.println(tagId, HEX);

    //Realização do disparo contido na etiqueta
    fireError = pnrd.fire();
  }

  switch (fireError) {
    case FireError::NO_ERROR:
      Serial.println("Disparo bem sucedido.");

      //Mostrar o vetor de marcações resultante do disparo
      pnrd.printTokenVector();

      //Salvar a nova informação na etiqueta
      if (pnrd.saveData() == WriteError::NO_ERROR) {
        publish("NO_ERROR");
        Serial.println("Informação atualizada.");
      } else Serial.println("Erro na atualização da etiqueta.");

      break;
    case FireError::PRODUCE_EXCEPTION:
      publish("Exception");
      Serial.println("Erro: disparo gerou exceção.");

      break;
    case FireError::CONDITIONS_ARE_NOT_APPLIED:
      publish("Error: 001");
      Serial.println("Erro: condições não são satisfeitas.");

      break;
  }
}

void publish(String error) {
  char text[20];

  snprintf(text, 20, "%s", tagId);
  while (!MQTT.publish("PELMS-MQTT/Runtime/id", text))
    if (!MQTT.connected()) conectarMQTT();

  while (!MQTT.publish("PELMS-MQTT/Runtime/reader", pelmsReader.c_str()))
    if (!MQTT.connected()) conectarMQTT();

  snprintf(text, 20, "%s", error);
  while (!MQTT.publish("PELMS-MQTT/Runtime/error", text))
    if (!MQTT.connected()) conectarMQTT();

  while (!MQTT.publish("PELMS-MQTT/Runtime/antenna", pelmsAntenna.c_str()))
    if (!MQTT.connected()) conectarMQTT();

  while (!MQTT.publish("PELMS-MQTT/Runtime/fire", pelmsPosition.c_str()))
    if (!MQTT.connected()) conectarMQTT();
}

/* MQTT FUNCTION FOR CONNECT TO SERVER */
void conectarMQTT() {
  // printf("%s\n", MQTTClientid);
  while (!MQTT.connected())
    if (MQTT.connect(MQTTClientid)) MQTT.subscribe(topic);
}

/* RESIZE THE MATRIX */
void resize(int8_t *&original, int setSIZE, String msg) {
	int8_t *temporiginal = new int8_t[setSIZE];
  int j = 0;
  volatile bool flag = false;

	for (int i = 0; i < msg.length(); i++) {
    String text = String(msg.charAt(i));
    if (strcmp(text.c_str(), "{") && strcmp(text.c_str(), ",") && strcmp(text.c_str(), " ") && strcmp(text.c_str(), "}") && strcmp(text.c_str(), "-")) {
		  temporiginal[j] = flag ? (-text.toInt()):(text.toInt());
      flag = false;
      j++;
    } else if (!strcmp(text.c_str(), "-")) {
      flag = true;
    }
  }

	delete[] original;
	original = temporiginal; //point old array to new array
}

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