#!/usr/bin/python3
'''
Created on Nov, 2021
Updated on:
  * Jan, 2022
  * Dec, 2024
@author: Roger Henrique Carrijo de Paula
@updater author:
  * Daniel Barbosa Pereira
  * Álisson Carvalho Vasconcelos
@Github authors:
  * rogercarrijo
  * daniel-b-pereira
  * AlissonCV
'''

# Import System Class
import os
import sys

# Import MQTT Json Class
import json

# Import Time Class
from datetime import datetime as dt
from time import sleep

# Importing Pyqt5 Class
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Import GUI Class
from gui.MainWindow import Ui_MainWindow
from gui.PopupInfo import PopupInfo

from pelms.Pnrd import Pnrd
from pelms.FileCreator import FileCreator
from pelms.FileCopy import FileCopy
from pelms.utils.template import *

from paho.mqtt import client as mqtt_client

class PelmsGui():
    # def __init__
    # def connect_MQTT
    # def PNRD_setup
    # def open_pnml_file
    # def PNRD_pelms_runtime
    # def open_pelms_file
    # def create_PELMS_file
    # def setup_PELMS_type
    # def append_reader
    # def get_transition_names
    # def set_antennas
    # def setup_matrix_view
    # def setup_matrix_vector
    # def setup_marking_vector
    # def publish_mqtt
    # def transferPNRD
    # def publish_inicial
    # def receive_mqtt
    # def mqtt_fire
    def __init__(self):
        self.pathName = ''
#        self.MQTT_array = {}

#------------------------------------------------ PELMS MQTT Variables ------------------------------------------------
        #--------------------------------------------    MQTT Variables    --------------------------------------------
        #self.brokerName = 'Mosquitto'
        #self.broker = 'test.mosquitto.org'
        #self.brokerName = 'MAPL'
        #self.broker = '200.19.144.16'
        self.brokerName = 'RPi-MAPL'
        self.broker = '192.168.1.13'
        #self.brokerName = 'RPi-MAPL'
        #self.broker = '192.168.12.9'
        self.port = 1883
        self.username = 'XXXX'
        self.password = 'XXXX'

        self.client_id = 'PELMS'
        self.topic = {
            'place': 'PELMS-MQTT/len_place',
            'transition': 'PELMS-MQTT/len_transition',
            'token': 'PELMS-MQTT/marking_vector',
            'incidence': 'PELMS-MQTT/incidence_matrix',
            'fire': 'PELMS-MQTT/fire_vector',
            'runtime': 'PELMS-MQTT/Runtime/'
        }

        self.client = mqtt_client.Client(self.client_id)
        self.mqtt_runtime_flag = 'OFF'
        self.pnrd_mqtt = dict()

        #--------------------------------------------    PNRD Variables    --------------------------------------------
        self.pnrd = Pnrd()
        self.pnrd_setup_is_ok = False
        self.pelms_type = ''

        #-------------------------------------------- Petri Net Variables  --------------------------------------------
        self.count_antenna = 0
        self.qtd_antena = 0
        self.reader_list = []
        self.transition_names = []
        self.array_matrix = []
        self.array_marking= []
        self.starting_token_vector = []

#------------------------------------------ PELMS MainWindow Implementation  ------------------------------------------
        #-------------------------------------------- MainWindow Creation  --------------------------------------------
        app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        #----------------------------------------------- File Open Menu -----------------------------------------------
        self.ui.actionopen_pnml.triggered.connect(self.open_pnml_file)
        self.ui.actionOpen_Setup_File_pelms.triggered.connect(self.open_pelms_file)

        #-------------------------------------------- Setup PNRD Type List --------------------------------------------
        self.ui.setupPelms_comboBox.currentIndexChanged.connect(self.setup_PELMS_type)

        #------------------------------------------------- Add Button -------------------------------------------------
        self.ui.addIP_pushButton.clicked.connect(self.append_reader)

        #---------------------------------------- Export PELMS Setup Button  ------------------------------------------
        self.ui.createSetup_pushButton.clicked.connect(self.create_PELMS_file)

        #------------------------------------------ Setup Antenna Input Box  ------------------------------------------
        self.ui.nAntennas_spinBox.setMinimum(1)
        self.ui.nAntennas_spinBox.setMaximum(3)
        self.ui.nAntennas_spinBox.setValue(1)

        #---------------------------------------- Transfer PNRD Setup Button ------------------------------------------
        self.ui.transferPNRDSetup_pushButton.clicked.connect(self.transferPNRD)

        #------------------------------------------ Get Runtime Info Button  ------------------------------------------
        self.ui.getRuntimeInfo_pushButton.clicked.connect(self.receive_mqtt)

        #---------------------------------------- Transfer Initial Data Button ----------------------------------------
        self.ui.generateNewPNML_pushButton.clicked.connect(self.publish_inicial)

        #------------------------------------------ Display PELMS MQTT Window  ----------------------------------------
        self.MainWindow.show()
        sys.exit(app.exec_())

#----------------------------------------------- Connect to MQTT Server -----------------------------------------------
    def connect_MQTT(self):
        #----------------------------------------------- Connect Event  -----------------------------------------------
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Connected to {self.brokerName} Broker!")
                client.subscribe(f'{self.topic["runtime"]}#')
            else:
                print(f"Failed to connect, return code %d\n", rc)
            
        #----------------------------------------------- Message Event  -----------------------------------------------
        def on_message(client, userdata, msg):
            if self.mqtt_runtime_flag == "ON":
                print(f'Recebido \"{msg.payload.decode()}\" de \"{msg.topic}\" topic')

                if f'{self.topic["runtime"]}id' == msg.topic:
                    self.pnrd_mqtt['id'] = msg.payload.decode()
                    self.ui.id_label.setText("TagId: "+str( self.pnrd_mqtt['id']))
                elif f'{self.topic["runtime"]}reader' == msg.topic:
                    self.pnrd_mqtt['reader'] = msg.payload.decode()
                    self.ui.reader_label.setText("Reader: "+str( self.pnrd_mqtt['reader']))
                elif f'{self.topic["runtime"]}error' == msg.topic:
                    self.pnrd_mqtt['error'] = msg.payload.decode()
                    self.ui.exception_label.setText("PNRD: "+str( self.pnrd_mqtt['error']))
                elif f'{self.topic["runtime"]}antenna' == msg.topic:
                    self.pnrd_mqtt['antenna'] = msg.payload.decode()
                elif f'{self.topic["runtime"]}fire' == msg.topic:
                    self.pnrd_mqtt['fire'] = msg.payload.decode()
                    self.pnrd_mqtt['date'] = dt.now().strftime("%m/%d/%Y")
                    self.pnrd_mqtt['time'] = dt.now().strftime("%H:%M:%S")

                    self.ui.incMatrix2_tw.item(self.count_col, self.pnrd.len_places).setBackground(QColor('White'))
                    self.count_col = int(self.pnrd_mqtt['fire'])
                    if self.pnrd_mqtt['error'].lower() == "no_error":
                        self.ui.incMatrix2_tw.item(self.count_col, self.pnrd.len_places).setBackground(QColor('LightGreen'))
                        self.mqtt_fire(self.pnrd_mqtt['fire'])
                    elif self.pnrd_mqtt['error'].lower() == "exception":
                        self.ui.incMatrix2_tw.item(self.count_col, self.pnrd.len_places).setBackground(QColor('Tomato'))
                    else:
                        self.ui.incMatrix2_tw.item(self.count_col, self.pnrd.len_places).setBackground(QColor('Gold'))

                    #print(self.pnrd_mqtt)
                    runtime = FileCreator('pelmsSetup/runtime', self.pathName, 'runtime', 'pnrd')
                    runtime.set_text_increment(
                        template_mqtt(
                            tagid = self.pnrd_mqtt['id'],
                            reader = self.pnrd_mqtt['reader'],
                            error = self.pnrd_mqtt['error'],
                            antenna = self.pnrd_mqtt['antenna'],
                            fire = self.pnrd_mqtt['fire'],
                            date = self.pnrd_mqtt['date'],
                            time = self.pnrd_mqtt['time']
                        )
                    )

        #-------------------------------------------- Server MQTT Variable --------------------------------------------
        if self.username != 'XXXX' and self.password != 'XXXX':
            self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

#--------------------------------------------------- Open PNML File ---------------------------------------------------
    #--------------------------------------- Run Petri Net and call for display ---------------------------------------
    def PNRD_setup(self, fileName):
        _,success = self.pnrd.set_pnml(self.pathName + fileName)
        if success:
            _,success = self.pnrd.create_net()
            if success:
                self.setup_matrix_view(self.pnrd.len_transitions,self.pnrd.len_places)
                self.setup_matrix_vector()
                self.setup_marking_vector(self.pnrd.len_places)
                self.pnrd_setup_is_ok = True
                self.count_antenna = self.pnrd.len_transitions
                self.ui.nAntennas_spinBox.setRange(1, 3)
                self.ui.qtdTotalTansitions_label.setText(f'(Left: {self.count_antenna})')
                self.setup_PELMS_type()

    #----------------------------------------------- Run Open PNML File -----------------------------------------------
    def open_pnml_file(self):
        self.ui.createSetup_pushButton.setEnabled(True)

        self.ui.addIP_pushButton.setEnabled(True)

        self.fileName, _ = QFileDialog.getOpenFileName(filter ="PNML (*.pnml)")
        self.pathName = os.path.dirname(os.path.abspath(self.fileName))
        self.fileName = (self.fileName.split('/'))[-1].replace('.pnml', '')

        self.ui.setup_tabWidget.setCurrentIndex(0)
        self.ui.setup_tabWidget.setTabEnabled(0, True)
        self.ui.setup_tabWidget.setTabEnabled(1, False)

        self.ui.readerName_lineEdit.setText('')
        self.ui.qtdTotalTansitions_label.setText('(Left: 0)')
        self.ui.nAntennas_spinBox.setRange(0, 0)
        self.ui.IP_lineEdit.setText('')
        self.ui.setupInfo_label.setText('')
        self.ui.markingVector_tw.setRowCount(0)
        self.ui.markingVector_tw.setColumnCount(0)
        self.ui.incMatrix_tw.setRowCount(0)
        self.ui.incMatrix_tw.setColumnCount(0)
        self.ui.matrix_array.setText('')
        self.ui.marking_array.setText('')
        self.text_setup = ''
        self.reader_list = []

        if self.fileName !='':
            self.PNRD_setup(f'/{self.fileName}.pnml')

#-------------------------------------------------- Open PELMS File  --------------------------------------------------
    #--------------------------------------- Run Petri Net and call for display ---------------------------------------
    def PNRD_pelms_runtime(self, fileName):
        with open(self.pathName + fileName, 'r')as pelms_file:
            pelms = json.load(pelms_file)
            _,success = self.pnrd.set_pnml(pelms["pnmlFile"])
            if success:
                _,success = self.pnrd.create_net()
                if success:
                    self.pnrd.transition_names = pelms["transitionNames"]
                    self.setup_matrix_view(self.pnrd.len_transitions,self.pnrd.len_places,"pelms")
                    self.setup_matrix_vector("pelms")
                    self.setup_marking_vector(self.pnrd.len_places,"pelms")
                    self.pnrd_setup_is_ok = True
                    self.setup_PELMS_type()
                    self.ui.pelmsType_label.setText(f'Type: {pelms["type"]}')
                    self.ui.qtdReader_label.setText(f'Qtd Readers: {pelms["qtdReaders"]}')
                    readers_list = ''
                    for i in pelms["readerListConfig"]:
                        readers_list += f'Reader: {i["readerName"]} \n  Qtd Ant:{i["qtdAntenna"]} \n  IP: {i["IP"]}\n\n' 

                    self.ui.readerList_label.setText(readers_list)
                    self.reader_list = pelms["readerListConfig"]
                    self.pelms_type = pelms["type"]

    #---------------------------------------------- Run Open PELMS File  ----------------------------------------------
    def open_pelms_file(self):
        self.fileName, _ = QFileDialog.getOpenFileName(filter ="PELMS (*.pelms)")
        self.pathName = (os.path.dirname(os.path.abspath(self.fileName))).replace("/pelmsSetup", "")
        fileName = self.fileName.replace(self.pathName, "")
        self.fileName = self.pathName.split('/')[-1]

        self.ui.setup_tabWidget.setCurrentIndex(1)
        self.ui.setup_tabWidget.setTabEnabled(1, True)
        self.ui.setup_tabWidget.setTabEnabled(0, False)
        
        if fileName !='':
            self.PNRD_pelms_runtime(fileName)
            self.connect_MQTT()
            self.count_col = 0

#------------------------------------------------- Create PELMS Files -------------------------------------------------
    # TODO
    def create_PELMS_file(self):
        path = (f'{QFileDialog.getSaveFileName(directory = self.fileName, filter ="All Files (*.*)", )[0]}').replace(f'{self.fileName}/','') if 'PNMLexamples' in self.pathName else self.pathName
        path = path if self.fileName in path else f'{path}/{self.fileName}'
        self.pelms_type = self.ui.setupPelms_comboBox.currentText()
        self.get_transition_names(self.pnrd.len_transitions,self.pnrd.len_places)

        pelms_file = FileCopy(path, self.pathName, self.fileName, self.fileName, 'pnml')
        pelms_file.copy_file() if 'PNMLexamples' in self.pathName else pelms_file.move_file()
        pelms_file = FileCreator('pelmsSetup', path,'setup','pelms')
        dict_pelms = {
            "pnmlFile": self.pnrd.file,
            "type": self.pelms_type,
            "qtdReaders":len(self.reader_list),
            "readerListConfig": self.reader_list,
            "transitionNames": self.transition_names
        }
        pelms_file.set_text(json.dumps(dict_pelms, indent=4, sort_keys=True))

        fileName = f'{self.pelms_type.lower()}Data'
        pnrd_data = FileCreator('pelmsSetup', path, fileName, 'pnrd')
        pnrd_data.set_text(
            template_pnrd_data(
                n_places = self.pnrd.len_places,
                n_transitions = self.pnrd.len_transitions,
                IncidenceMatrix = ','.join(map(str, self.array_matrix)),
                StartingTokenVector = ','.join(map(str, self.starting_token_vector)),
                FireVector = None if self.pelms_type.lower() == 'pnrd' else ('1' if i == 0 else ',0' for i in range(self.pnrd.len_transitions))
            )
        )

        fileName = f'{self.pelms_type.lower()}_recorder'
        reader_ino = FileCreator(f'pelmsSetup/ino/{fileName}', path, fileName, 'ino')
        reader_ino.set_text(template_recorder(self.pelms_type, self.topic))
        wifi_h = FileCreator(f'pelmsSetup/ino/{fileName}', path, 'WiFiPassword','h')
        wifi_h.set_text(
            template_recorder_h(
                'TROJANUBL',
                'CABRAL12',
                'ESP32-RECORDER',
                self.broker,
                1883,
                1,
                self.topic['runtime'].replace('Runtime/','#')
            )
        )

        i = 0
        antenna_id_list = ""
        reader_list = list()

        for reader in self.reader_list:
            fileName = f'{self.pelms_type.lower()}_reader_{i}' if len(self.reader_list) > 1 else f'{self.pelms_type.lower()}_reader'
            reader_ino = FileCreator(f'pelmsSetup/ino/{fileName}', path, fileName, 'ino')
            reader_ino.set_text(template_reader(self.pelms_type, self.topic))
            wifi_h = FileCreator(f'pelmsSetup/ino/{fileName}', path, 'WiFiPassword', 'h')

            reader_list.append(f'pelms {i}') if reader["readerName"] == '' else reader_list.append(reader["readerName"])
            antenna_list = list()
            position_list = list()
            for count in range(reader["qtdAntenna"]):
                antenna_list.append(count)
                position_list.append(i + count)
            antenna_id_list += f'{"" if i == 0 and i < len(reader) else ","}{antenna_list}'

            wifi_h.set_text(
                template_reader_h(
                    'TROJANUBL',
                    'CABRAL12',
                    'ESP32-RECORDER',
                    self.broker,
                    1883,
                    1,
                    self.topic['runtime'].replace('Runtime/','#'),
                    reader_list[i],
                    ",".join(map(str, antenna_list)),
                    i
                )
            )

            i += 1

        self.ui.popup_info = PopupInfo("Successfully created PELMS file!\nTo open file and use runtime mode press (Ctrl + F)")
        self.ui.popup_info.show()
        self.ui.createSetup_pushButton.setEnabled(False)

        self.ui.addIP_pushButton.setEnabled(False)
        self.text_setup = ''

#-------------------------------------------------- Setup PNRD Type  --------------------------------------------------
    def setup_PELMS_type(self):
        self.pelms_type = self.ui.setupPelms_comboBox.currentText()
        if self.pelms_type=='iPNRD':
            self.ui.nAntennas_spinBox.setMinimum(1)
            self.ui.nAntennas_spinBox.setMaximum(1)
        if self.pelms_type=='PNRD':
            self.ui.nAntennas_spinBox.setMinimum(1)
            self.ui.nAntennas_spinBox.setMaximum(3)

        self.ui.qtdTotalTansitions_label.setText(f'(Left: {self.count_antenna})')

        return self.pelms_type

#---------------------------------------- Display Create Setup File Menu Text  ----------------------------------------
    def append_reader(self):
        pelms_type = self.setup_PELMS_type()
        reader_name = self.ui.readerName_lineEdit.text()

        #- TODO: config that the same IP cannot be used twice -#
        ip_connection = self.ui.IP_lineEdit.text() if self.ui.IP_lineEdit.text() != self.broker else f'{self.broker.replace(self.broker[-1], str(int(self.broker[-1]) + 1))}'
        self.ui.IP_lineEdit.setText(ip_connection)

        if pelms_type =='PNRD':
            self.set_antennas()
#            print(f"Antenna Used: {self.qtd_antena}\tAntenna Left: {self.count_antenna}")

            self.reader_list.append({"readerName":reader_name,"qtdAntenna":self.qtd_antena,"IP":ip_connection})

            self.text_setup += f"\nReader: {reader_name} IP: '{ip_connection}' Ant: {self.qtd_antena} units"
        else:
            self.set_antennas()
#            print(f"Antenna Used: {self.qtd_antena}\tAntenna Left: {self.count_antenna}")

            self.reader_list.append({"readerName":reader_name,"qtdAntenna":1,"IP":ip_connection})

            self.text_setup += f"\nReader: {reader_name} IP: '{ip_connection}' Ant: 1 unit"

        self.ui.setupInfo_label.setText(f'P: {self.pnrd.len_places} | T: {self.pnrd.len_transitions}{self.text_setup}')

#------------------------------------------- Get Transition Names Displayed -------------------------------------------
    def get_transition_names(self,n_row,n_col):
        self.transition_names = []
        for i in range(n_row):
            matrix_transition_item = self.ui.incMatrix_tw.item(i,n_col)
            self.transition_names.append(matrix_transition_item.text())

#------------------------------------------- Count and Limit Qtd of Antenna -------------------------------------------
    def set_antennas(self):
        if self.count_antenna >= self.ui.nAntennas_spinBox.value():
            self.count_antenna -=self.ui.nAntennas_spinBox.value()
            self.qtd_antena = self.ui.nAntennas_spinBox.value()

        if self.count_antenna > 0:
            self.setup_PELMS_type()
        elif self.count_antenna == 0:
            self.ui.nAntennas_spinBox.setMaximum(0)
            self.ui.nAntennas_spinBox.setMinimum(0)
            self.ui.qtdTotalTansitions_label.setText(f'(Left: {self.count_antenna})')
            self.ui.addIP_pushButton.setEnabled(False)

#----------------------------------------- Display the Incidence Matrix Table -----------------------------------------
    def setup_matrix_view(self,n_row,n_col,_type="pnml"):
        self.ui.incMatrix2_tw.setRowCount(n_row) if _type == "pelms" else self.ui.incMatrix_tw.setRowCount(n_row)
        self.ui.incMatrix2_tw.setColumnCount(n_col+1) if _type == "pelms" else self.ui.incMatrix_tw.setColumnCount(n_col+1)

        count_row = 0
        horizontalHeader = []
        verticalHeader = []

        for row in self.pnrd.incidence_matrix:
            count_col = 0
            for i in row:
                    if len(horizontalHeader) < n_col:
                        horizontalHeader.append(f" P{count_col} ")

                    if count_col==(n_col -1):
                        self.ui.incMatrix2_tw.setItem( count_row,count_col+1, QTableWidgetItem(f'{self.pnrd.transition_names[count_row]}')) if _type == "pelms" else self.ui.incMatrix_tw.setItem( count_row,count_col+1, QTableWidgetItem(f'transition {count_row}'))

                    self.ui.incMatrix2_tw.setItem( count_row,count_col, QTableWidgetItem(f"{i}")) if _type == "pelms" else self.ui.incMatrix_tw.setItem( count_row,count_col, QTableWidgetItem(f"{i}"))

                    count_col+=1                 

            verticalHeader.append(f" T{count_row} ")
            count_row += 1

        horizontalHeader.append(f"  ")

        self.ui.incMatrix2_tw.setHorizontalHeaderLabels(horizontalHeader) if _type == "pelms" else self.ui.incMatrix_tw.setHorizontalHeaderLabels(horizontalHeader)
        self.ui.incMatrix2_tw.setVerticalHeaderLabels(verticalHeader) if _type == "pelms" else self.ui.incMatrix_tw.setVerticalHeaderLabels(verticalHeader)

        self.ui.places_label.setText(f'Places: {self.pnrd.len_places}') if _type == "pelms" else None
        self.ui.transitions_label.setText(f'Transitions: {self.pnrd.len_transitions}') if _type == "pelms" else None

#------------------------------------ Display the Incidence Matrix Transpose Array ------------------------------------
    def setup_matrix_vector(self,_type="pnml"):
        self.array_matrix = []

        for row in self.pnrd.incidence_matrix_t:
            for pos in row:
                    self.array_matrix.append(pos)

        None if _type == "pelms" else self.ui.matrix_array.setText(f"{self.array_matrix}")

#-------------------------------------------------- Display the Marking Vector Table --------------------------------------------------
    def setup_marking_vector(self,n_row,_type="pnml"):
        self.ui.markingVector2_tw.setRowCount(n_row) if _type == "pelms" else self.ui.markingVector_tw.setRowCount(n_row)
        self.ui.markingVector2_tw.setColumnCount(1) if _type == "pelms" else self.ui.markingVector_tw.setColumnCount(1)

        count_row = 0
        verticalHeader = []
        self.array_marking= []
        self.starting_token_vector = []

        for i in self.pnrd.marking_vector:
            # TODO: Confirm if the starting token vector in pnml is the first position
            self.starting_token_vector.append(i)

            verticalHeader.append(f" P{count_row} ")

            self.ui.markingVector2_tw.setItem(count_row,0, QTableWidgetItem(f"{i}")) if _type == "pelms" else self.ui.markingVector_tw.setItem(count_row,0, QTableWidgetItem(f"{i}"))
            if 1 == i and _type == "pelms":
                self.ui.markingVector2_tw.item(count_row, 0).setBackground(QColor('LightGreen'))


            self.array_marking.append(i)
            count_row+=1

        self.ui.markingVector2_tw.setHorizontalHeaderLabels([""]) if _type == "pelms" else self.ui.markingVector_tw.setHorizontalHeaderLabels([""])
        self.ui.markingVector2_tw.setVerticalHeaderLabels(verticalHeader) if _type == "pelms" else self.ui.markingVector_tw.setVerticalHeaderLabels(verticalHeader)

    #---------------------------------------- Display the Marking Vector Array ----------------------------------------
        None if _type == "pelms" else self.ui.marking_array.setText(f"{self.array_marking}")
        
#--------------------------------------------- MQTT Publishing PELMS DATA ---------------------------------------------
    #------------------------------------------ Call Publish PNRD to Reader  ------------------------------------------
    def transferPNRD(self):
        self.publish_mqtt(f'pelmsSetup/{self.pelms_type.lower()}Data.pnrd', True)

    #----------------------------------------- Call Publish PNRD to Recorder  -----------------------------------------
    def publish_inicial(self):
        self.publish_mqtt(f'pelmsSetup/{self.pelms_type.lower()}Data.pnrd')

    #---------------------------------------------- Publish PNRD Message ----------------------------------------------
    def publish_mqtt(self, fileName, type = False):
        with open(self.pathName + f'/{fileName}', 'r') as mqtt:
            file_text = mqtt.read().splitlines()
            topic = ""

            for i in range(len(file_text)):
                for j in self.topic.keys():
                    if j in file_text[i]:
                        text_mqtt = file_text[i].replace(f'{j}: ','')
                        #print(f'{j}, {text_mqtt}')

                        if type:
                            topic = self.topic[j].split('/')
                            topic = self.topic[j].replace(topic[-1], f'fire/{topic[-1]}')
                        else:
                            topic = self.topic[j]

                        result = self.client.publish(topic, text_mqtt)
                        sleep(0.05)

                        if not result[0]:
                            print(f"Sucess to send message to topic {topic}")
                        else:
                            print(f"Failed to send message to topic {topic}")

            mqtt.close()

#------------------------------------------ MQTT Receive PELMS Runtime Data  ------------------------------------------
    def receive_mqtt(self):
        self.mqtt_runtime_flag = 'ON'

#------------------------------------------------ Fire Petri Nets View ------------------------------------------------
    def mqtt_fire(self, fire_position):
        fire_position = fire_position.replace(f'{fire_position}', f'transition {fire_position}')

        count_row = 0
        for row in range(self.pnrd.len_transitions):
            matrix_transition_item = self.ui.incMatrix2_tw.item(row, self.pnrd.len_places)
            if fire_position == matrix_transition_item.text():
                break
            count_row += 1

        count_col = [0, 0]
        flag = [False, False]
        for col in self.pnrd.incidence_matrix[count_row]:
            if abs(col) != 1:
                count_col[0] += 1 if not flag[0] else 0
                count_col[1] += 1 if not flag[1] else 0
            elif col == -1:
                flag[0] = True
                count_col[1] += 1 if not flag[1] else 0
            elif col == 1:
                flag[1] = True
                count_col[0] += 1 if not flag[0] else 0
            
            if flag[0] and flag[1]:
                break

        self.ui.markingVector2_tw.setItem(count_col[0], 0, QTableWidgetItem("0"))
        self.ui.markingVector2_tw.setItem(count_col[1], 0, QTableWidgetItem("1"))
        self.ui.markingVector2_tw.item(count_col[0], 0).setBackground(QColor('White'))
        self.ui.markingVector2_tw.item(count_col[1], 0).setBackground(QColor('LightGreen'))

#-------------------------------------------- Run if the file is the main  --------------------------------------------
if __name__ == "__main__":
    PelmsGui()