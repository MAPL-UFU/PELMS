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

/** DEFINITION OF WiFi DATA
 * Definition of macros SSID, username and password
*/
#define SSID "PELMSVAR01"
#define username "PELMSVAR02"
#define password "PELMSVAR03"
#define anonymous "PELMSVAR04"

/** DEFINITION OF MQTT DATA
 * Definition of macros MQTTClientid, MQTTServer and MQTTPort
*/
#define MQTTClientid "PELMSVAR05"
#define MQTTServer "PELMSVAR06"
#define MQTTPort PELMSVAR07

/* DEFINITION OF READER PORT INPUT */
#define port PELMSVAR08

/* DECLARATION OF TOPICS VARIABLES */
const char* topic = "PELMSVAR09";