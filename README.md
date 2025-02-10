# ![PELMS LOGO](ico.ico) PELMS

PELMS or Petri Net Inside RFID Database Management System implemented in ESP32 is a middleware able to integrate Petri net modeling tools (through the use of pnml exported file) with PNRD/iPNRD (Petri Net Inside RFID Database/inverted Petri Net Inside RFID Database). In this version of PELMS, it can be connected to as many ESP32 as available through MQTT connection. Each ESP32 can connect to one or more PN532 RFID readers. As internal structure, PELMS has two modes, it means, Setup and Runtime.

## SETUP MODE

The feature of Setup mode is pnml convertion and the generation of a 'setup.pelms' file as intermediary of PNML and PNRD/iPNRD relationship. ESP32's templates files are stored in "pelms/utils" directory. Attention: There are two distincts ESP32's files in "pelms/utils" directory, one for tag recording initial marking (template_recorder.ino) and another for reader setup (template_reader.ino), and both must be compiled by Arduino IDE manually. PELMS create automaticaly '.pnrd' files with PNRD data structure and this file allows PELMS update PNRD information in "real-time" using MQTT protocol.

## RUNTIME MODE
In the Runtime mode PELMS transfer the Petri Net information to the connected ESP32 by MQTT protocol, and receive the data generated from the readers with next state calculus files. Based on these informations, marking vector is updated as well as a runtime history "json". If an exception is identified, PELMS shows it in its visual interface. Pnml is updated in order to visualize the whole process through any Petri net modelling tool which is able to read this format. PELMS follows "pnml" format. PELMS does not deal with exception treatment.

## USING PELMS

1. Install Python3

    sudo apt update
    sudo apt upgrade -y
    sudo apt install python3

2. Install PIP

    ```python
    pip install python3-pip

3. Install pip requirements

    ```python
    pip install -r requirements.txt
    ```

    ```python
    pip3 install -r requirements.txt
    ```

4. Execute script

    ```python
    python main.py
    ```


## COMPILING EXECUTABLE ON WINDOWS
Although the method above is preferable and also applicable for windows OS, a second way to run the software is building the executable .exe:

1. Install Pyinstaller
    ```python
    pip install pyinstaller
    ```
2. Execute script
    ```python
    pyinstaller --onefile -w main.py
    ```
The execuble built is found in the dist directory.

# PNRD/iPNRD ESP32 Library
For acces of full PNRD/iPNRD ESP32 Library you need to access [PNRD-ESP32-Library page](https://github.com/MAPL-UFU/PNRD-ESP32-Library) and install the library in Arduino IDE.

# License information
PELMS is licensed under The MIT License (MIT). Which means that you can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software. But you always need to state that MAPL-UFU is the original author of this software.

This project was started by Roger Carrijo, MQTT versions was developed by Daniel Barbosa Pereira and upgraded by Álisson Carvalho Vasconcelos.