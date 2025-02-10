String status = "", topic_status = "";
int sizearray[] = {1, 2};

/** Input of Incidence Matrix
 * The size of Incidence Matrix must contain the number of transitions and the number of places in PetriNet
*/
int8_t* mIncidenceMatrix = new int8_t[2]{-1,1};

/** Input of Token Vector
 * The size of Token Vector must contain the number of places in PetriNet
*/
uint16_t* mStartingTokenVector = new uint16_t[2]{1,0};

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
    else break;
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
    if (!strcmp(msg_topic.c_str(), "PELMSVAR1")) {
      sizearray[0] = msg.toInt();
    } else if (!strcmp(msg_topic.c_str(), "PELMSVAR2")) {
      sizearray[1] = msg.toInt();
    } else if (!strcmp(msg_topic.c_str(), "PELMSVAR3")) {
      resize(mStartingTokenVector, sizearray[0], msg);
    } else if (!strcmp(msg_topic.c_str(), "PELMSVAR4")) {
      resize(mIncidenceMatrix, sizearray[0]*sizearray[1], msg);

      // printf("Places: %d\nTransition: %d\nIncidence Matrix: {", sizearray[0], sizearray[1]);
      // for (int i = 0; i < (sizearray[0]*sizearray[1]); i++)
        // i == (sizearray[0]*sizearray[1] - 1) ? printf("%d}\nMarking Vector: {", mIncidenceMatrix[i]):printf("%d, ", mIncidenceMatrix[i]);
      // for (int i = 0; i < sizearray[0]; i++)
        // i == (sizearray[0] - 1) ? printf("%d}\n", mStartingTokenVector[i]):printf("%d, ", mStartingTokenVector[i]);
      printf("Starting Tag Recording!!\n");

      // Preparing the tag information
      eraseRFID();
      cleanRFID();
      formatRFID();
      recordRFID();
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

  printf("Please place the Tag!!!\n");

  // Identifier if tag is present
  while (!nfc.tagPresent()) delay(500);
  
  tag.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
  for(int i = 0; i < uidLength; i++) tagID += String(uid[i], HEX);
  tagID.toUpperCase();
  printf("Tag Presented (TagID: %s)!!!\n", tagID);

  // Erase the tag returning the success of erasing
  printf("Erasing the Tag.\n");
  bool success = nfc.erase();

  // Return the message of erasing
  printf(success ? "Tag erased successfully.\n":"Error to erasing the tag!\n");
}

void cleanRFID() {
  nfc.begin();

  // Identifier if tag is present
  while (!nfc.tagPresent()) delay(500);

  // Return the tag do Factory and returning the success of Factory Setup
  printf("Restoring the tag to factory setup.\n");
  
  bool success = nfc.clean();

  printf(success ? "Successfully restoring the tag to factory setup.\n":"Tag is already in factory setup!\n");
}

void formatRFID() {
  nfc.begin();

  // Identifier if tag is present
  while (!nfc.tagPresent()) delay(500);

  // Format the tag returning the success of formating
  printf("Formating the Tag to NDEF format.\n");
  
  bool success = nfc.format();

  printf(success ? "Tag successfully formated as NDEF format.\n":"Tag is already formated as NDEF format!\n");
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

  //Defining the Incidence Matrix and the Token Vector to be recorded
  pnrd.setIncidenceMatrix(mIncidenceMatrix);
  pnrd.setTokenVector(mStartingTokenVector);

  //Setting of the classic PNRD approach
  pnrd.setAsTagInformation(PetriNetInformation::TOKEN_VECTOR);
  pnrd.setAsTagInformation(PetriNetInformation::ADJACENCY_LIST);
  Serial.print("\nInitial recording of PNRD tags.\n");

  // Identifier if tag is present
  while (!nfc.tagPresent()) delay(500);

  printf("Storing the PNRD in Tag!\n");
  bool success = pnrd.saveData() == WriteError::NO_ERROR;
  // Cormfirming if data is saved
  printf(success ? "PNRD is stored in the tag!\n":"Error to storing PNRD in the tag!\n");
}

/* MQTT FUNCTION FOR CONECT TO SERVER */
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