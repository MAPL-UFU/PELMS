#!/usr/bin/python3
'''
Created on Nov, 2021
Updated on:
  * Jan, 2022
  * Dec, 2024
@author: Daniel Barbosa Pereira
@updater author:
  * Roger Henrique Carrijo de Paula
  * Daniel Barbosa Pereira
  * Álisson Carvalho Vasconcelos
@Github authors:
  * rogercarrijo
  * daniel-b-pereira
  * AlissonCV
'''

# Importing functions inside PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#-------------------------------------------------------------
from os import getcwd as path
import sys

# Function to get de directory
def resource_path(relative_path):
  if 'gui' in path():
    base_path = path() + relative_path
  else:
    base_path = path() + "/gui" + relative_path

  if (sys.platform == 'win32'):
    base_path = base_path.replace("/", "\\")

  return base_path
#-------------------------------------------------------------

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(931, 609)
        MainWindow.move(100, 100)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(50, 50))
        MainWindow.setStyleSheet(
          #Window Layout Color
          "QMainWindow {\n"
          "    background-color: DimGray;\n"
          "}\n"

          #Panel Background Color
          "QTabWidget {\n"
#          "    background-color: rgb(255, 255, 255);\n"
          "    background-color: transparent;\n"
#          "    border:1px solid rgb(221, 216, 216);\n"
          "}\n"

          #Panel Layout Design
          "QTabWidget::pane {\n"
          "    background-color: LightGray;\n"
          "    border:1px solid Dark;\n"
          "}\n"

          #Tab Bar Background Color
          "QTabWidget::tab-bar {\n"
          "    background-color: rgb(238, 238, 236);\n"
          "    border:1px solid rgb(221, 216, 216);\n"
          "    alignment: center;\n"
          "}\n"

          #Tab Bar Layout Design
          "QTabBar::tab {\n"
          "    color: White;\n"
          "    background-color: DimGray;\n"
          "    border: 1px solid Gray;\n"
          "    padding: 5px;\n"
          "    margin-bottom:0px;\n"
          "}\n"

          #Tab Bar Selected Layout Color
          "QTabBar::tab:selected {\n"
          "    background-color: LightGray;\n"
          "    color: Dark;\n"
          "}\n"

          #Markin Vector and Incidence Matrix Box Layout Color
          "QTableWidget {\n"
          "    background-color: White;\n"
          "    border:1px  solid DimGray;\n"
          "}\n"

          #
          "QTableWidget::section {\n"
          "    background-color: transparent;\n"
          "    border:0px solid transparent;\n"
          "}\n"

          #Header of Markin Vector and Incidence Matrix
          "QHeaderView {\n"
          "    background-color: white;\n"
          "}\n"

          #
          "QHeaderView::section {\n"
          "    background-color: white;\n"
          "}\n"

          #
          "QHeaderView::section:vertical {\n"
          "    background-color: white;\n"
          "}\n"

          #
          "QHeaderView::section:horizontal {\n"
          "    background-color:rgb(238, 238, 236);\n"
          "}\n"

          #Marking Vector and Incidence Matrix Menu Layout Color
          "QGroupBox#groupBoxMatrix, QGroupBox#markingGroupBox,QGroupBox#groupBoxMatrix2, QGroupBox#markingGroupBox2 {\n"
          "    border: 1px solid DimGray;\n"
          "    background-color: transparent;\n"
          "}\n"

          #
#          "QGroupBox#groupBox_Labels{\n"
#          "    background-color: white;\n"
#          "    border:0px ,solid ,rgb(186, 189, 182);\n"
#          "}\n"

          #Setup Type Layout Color
          "#setupBg_groupBox {\n"
          "    background-color: LightGray;\n"
          "    border:1px solid DimGray;\n"
          "}\n"

          #
          "#pelmsType_label {\n"
          "    color:rgb(2, 160, 200);\n"
          "    background-color: transparent;\n"
          "    font: 75 14pt \"Courier 10 Pitch\";\n"
          "}\n"

          #
          "#exception_label{\n"
          "    color:rgb(204, 0, 0);\n"
          "    background-color: transparent;\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "}\n"

          #
          "#reader_label {\n"
          "    color:rgb(60, 167, 61);\n"
          "    background-color: transparent;\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "}\n"

          #
          "#id_label {\n"
          "    color:rgb(48, 140, 198);\n"
          "    background-color: transparent;\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "}\n"

          #
          "#places_label {\n"
          "    color:rgb(60, 167, 61);\n"
          "    background-color: transparent;\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "}\n"

          #
          "#transitions_label {\n"
          "    color:rgb(60, 167, 61);\n"
          "    background-color: transparent;\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "}\n"

          #
          "#info_label {\n"
          "    color:rgb(204, 0, 0);\n"
          "    background-color: transparent;\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "}\n"

          #Text Box of Create Setup File Layout Design
          "#setupInfo_label {\n"
          "    background-color: white;\n"
          "    border: 1px solid DimGray;\n"
          "    color:rgb(60, 167, 61);\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "}\n"

          #CREATE SETUP FILE
          "#createSetup_pushButton {\n"
          "    background-color: DimGray;\n"
          "    color: White;\n"
          "    border: 1px solid Dark;\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "    font-weight:bold;\n"
          "}\n"

          #Add
          "#addIP_pushButton {\n"
          "    background-color: DimGray;\n"
          "    color: White;\n"
          "    border: 1px solid Dark;\n"
          "    font: 75 12pt \"Courier 10 Pitch\";\n"
          "    font-weight:bold;\n"
          "}\n"
        )
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_11 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.setup_tabWidget = QTabWidget(self.centralwidget)
        self.setup_tabWidget.setTabPosition(QTabWidget.South)
        self.setup_tabWidget.setTabShape(QTabWidget.Rounded)
        self.setup_tabWidget.setObjectName("setup_tabWidget")
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName("tab_setup")
        self.verticalLayout_5 = QVBoxLayout(self.tab_setup)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QLabel(self.tab_setup)
        self.label_5.setObjectName("label_5")
        self.label_5.setMaximumSize(QSize(230, 120))
#        self.label_5.setFrameShape(QFrame.NoFrame)
        self.label_5.setText("")
        self.label_5.setPixmap(QPixmap(resource_path("images/femec - Copia.jpeg")))
        self.label_5.setScaledContents(True)
        self.label_5.setAlignment(Qt.AlignLeft)
#        self.label_5.setWordWrap(False)
        self.verticalLayout_4.addWidget(self.label_5)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.bgPnrd_verticalLayout = QVBoxLayout()
        self.bgPnrd_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.bgPnrd_verticalLayout.setObjectName("bgPnrd_verticalLayout")
        self.setupBg_groupBox = QGroupBox(self.tab_setup)
        self.setupBg_groupBox.setMaximumSize(QSize(100, 16777215))
        self.setupBg_groupBox.setTitle("")
        self.setupBg_groupBox.setAlignment(Qt.AlignCenter)
        self.setupBg_groupBox.setObjectName("setupBg_groupBox")
        self.verticalLayout_8 = QVBoxLayout(self.setupBg_groupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_6 = QLabel(self.setupBg_groupBox)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_8.addWidget(self.label_6)
        self.setupPelms_comboBox = QComboBox(self.setupBg_groupBox)
        self.setupPelms_comboBox.setMinimumSize(QSize(0, 60))
        self.setupPelms_comboBox.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setKerning(True)
        self.setupPelms_comboBox.setFont(font)
        self.setupPelms_comboBox.setLayoutDirection(Qt.LeftToRight)
        self.setupPelms_comboBox.setObjectName("setupPelms_comboBox")
        self.setupPelms_comboBox.addItem("")
        self.setupPelms_comboBox.addItem("")
        self.verticalLayout_8.addWidget(self.setupPelms_comboBox)
        self.bgPnrd_verticalLayout.addWidget(self.setupBg_groupBox)
        self.horizontalLayout_6.addLayout(self.bgPnrd_verticalLayout)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_7 = QLabel(self.tab_setup)
        self.label_7.setMaximumSize(QSize(100, 16777215))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.readerName_lineEdit = QLineEdit(self.tab_setup)
        self.readerName_lineEdit.setMaximumSize(QSize(300, 16777215))
        self.readerName_lineEdit.setObjectName("readerName_lineEdit")
        self.horizontalLayout_9.addWidget(self.readerName_lineEdit)
        self.verticalLayout_9.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_8 = QLabel(self.tab_setup)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_10.addWidget(self.label_8)
        self.qtdTotalTansitions_label = QLabel(self.tab_setup)
        self.qtdTotalTansitions_label.setText("")
        self.qtdTotalTansitions_label.setObjectName("qtdTotalTansitions_label")
        self.horizontalLayout_10.addWidget(self.qtdTotalTansitions_label)
        self.nAntennas_spinBox = QSpinBox(self.tab_setup)
        self.nAntennas_spinBox.setObjectName("nAntennas_spinBox")
        self.horizontalLayout_10.addWidget(self.nAntennas_spinBox)
        self.verticalLayout_9.addLayout(self.horizontalLayout_10)
        self.label_3 = QLabel(self.tab_setup)
        self.label_3.setMaximumSize(QSize(400, 30))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_9.addWidget(self.label_3)
        self.IP_lineEdit = QLineEdit(self.tab_setup)
        self.IP_lineEdit.setObjectName("IP_lineEdit")
        self.verticalLayout_9.addWidget(self.IP_lineEdit)
        self.addIP_pushButton = QPushButton(self.tab_setup)
        self.addIP_pushButton.setMinimumSize(QSize(0, 40))
        self.addIP_pushButton.setMaximumSize(QSize(400, 16777215))
        self.addIP_pushButton.setObjectName("addIP_pushButton")
        self.verticalLayout_9.addWidget(self.addIP_pushButton)
        self.horizontalLayout_6.addLayout(self.verticalLayout_9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.setupInfo_label = QLabel(self.tab_setup)
        self.setupInfo_label.setMaximumSize(QSize(500, 16777215))
        self.setupInfo_label.setObjectName("setupInfo_label")
        self.verticalLayout_4.addWidget(self.setupInfo_label)
        self.createSetup_pushButton = QPushButton(self.tab_setup)
        self.createSetup_pushButton.setMinimumSize(QSize(0, 50))
        self.createSetup_pushButton.setMaximumSize(QSize(500, 16777215))
        self.createSetup_pushButton.setObjectName("createSetup_pushButton")
        self.verticalLayout_4.addWidget(self.createSetup_pushButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.markingGroupBox = QGroupBox(self.tab_setup)
        self.markingGroupBox.setMinimumSize(QSize(100, 0))
        self.markingGroupBox.setMaximumSize(QSize(130, 16777215))
        self.markingGroupBox.setLayoutDirection(Qt.LeftToRight)
        self.markingGroupBox.setTitle("")
        self.markingGroupBox.setAlignment(Qt.AlignCenter)
        self.markingGroupBox.setObjectName("markingGroupBox")
        self.verticalLayout_2 = QVBoxLayout(self.markingGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.marking_vector = QLabel(self.markingGroupBox)
        self.marking_vector.setMinimumSize(QSize(30, 30))
        self.marking_vector.setMaximumSize(QSize(120, 16777215))
        self.marking_vector.setLayoutDirection(Qt.LeftToRight)
        self.marking_vector.setAlignment(Qt.AlignCenter)
        self.marking_vector.setObjectName("marking_vector")
        self.verticalLayout_2.addWidget(self.marking_vector)
        self.markingVector_tw = QTableWidget(self.markingGroupBox)
        self.markingVector_tw.setMinimumSize(QSize(30, 0))
        self.markingVector_tw.setMaximumSize(QSize(120, 16777215))
        self.markingVector_tw.setRowCount(0)
        self.markingVector_tw.setColumnCount(0)
        self.markingVector_tw.setObjectName("markingVector_tw")
        self.markingVector_tw.horizontalHeader().setDefaultSectionSize(30)
        self.markingVector_tw.horizontalHeader().setMinimumSectionSize(30)
        self.markingVector_tw.horizontalHeader().setStretchLastSection(True)
        self.markingVector_tw.verticalHeader().setMinimumSectionSize(30)
        self.verticalLayout_2.addWidget(self.markingVector_tw)
        self.horizontalLayout_2.addWidget(self.markingGroupBox)
        self.groupBoxMatrix = QGroupBox(self.tab_setup)
        self.groupBoxMatrix.setMinimumSize(QSize(350, 0))
        self.groupBoxMatrix.setTitle("")
        self.groupBoxMatrix.setObjectName("groupBoxMatrix")
        self.verticalLayout = QVBoxLayout(self.groupBoxMatrix)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.groupBoxMatrix)
        self.label.setMaximumSize(QSize(16777215, 30))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.incMatrix_tw = QTableWidget(self.groupBoxMatrix)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.incMatrix_tw.sizePolicy().hasHeightForWidth())
        self.incMatrix_tw.setSizePolicy(sizePolicy)
        self.incMatrix_tw.setMinimumSize(QSize(250, 0))
        self.incMatrix_tw.setMaximumSize(QSize(16777215, 16777215))
        self.incMatrix_tw.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.incMatrix_tw.setAutoScroll(True)
        self.incMatrix_tw.setGridStyle(Qt.SolidLine)
        self.incMatrix_tw.setRowCount(0)
        self.incMatrix_tw.setColumnCount(0)
        self.incMatrix_tw.setObjectName("incMatrix_tw")
        self.incMatrix_tw.horizontalHeader().setVisible(False)
        self.incMatrix_tw.horizontalHeader().setCascadingSectionResizes(False)
        self.incMatrix_tw.horizontalHeader().setDefaultSectionSize(30)
        self.incMatrix_tw.horizontalHeader().setMinimumSectionSize(30)
        self.incMatrix_tw.horizontalHeader().setSortIndicatorShown(False)
        self.incMatrix_tw.horizontalHeader().setStretchLastSection(True)
        self.incMatrix_tw.verticalHeader().setDefaultSectionSize(30)
        self.incMatrix_tw.verticalHeader().setMinimumSectionSize(30)
        self.incMatrix_tw.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.incMatrix_tw)
        self.horizontalLayout_2.addWidget(self.groupBoxMatrix)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6") 
        self.label_4 = QLabel(self.tab_setup)
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.matrix_array = QLineEdit(self.tab_setup)
        self.matrix_array.setMinimumSize(QSize(500, 40))
        self.matrix_array.setAlignment(Qt.AlignCenter)
        self.matrix_array.setObjectName("matrix_array")
        self.verticalLayout_6.addWidget(self.matrix_array)
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_2 = QLabel(self.tab_setup)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        self.marking_array = QLineEdit(self.tab_setup)
        self.marking_array.setMinimumSize(QSize(0, 40))
        self.marking_array.setText("")
        self.marking_array.setAlignment(Qt.AlignCenter)
        self.marking_array.setObjectName("marking_array")
        self.verticalLayout_7.addWidget(self.marking_array)
        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.setup_tabWidget.addTab(self.tab_setup, "")
        self.tab_petrinet = QWidget()
        self.tab_petrinet.setObjectName("tab_petrinet")
        self.verticalLayout_10 = QVBoxLayout(self.tab_petrinet)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.groupBox_Labels = QGroupBox(self.tab_petrinet)
        self.groupBox_Labels.setMinimumSize(QSize(200, 0))
        self.groupBox_Labels.setMaximumSize(QSize(9999999, 16777215))
        self.groupBox_Labels.setTitle("")
        self.groupBox_Labels.setObjectName("groupBox_Labels")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_Labels)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pelmsType_label = QLabel(self.groupBox_Labels)
        self.pelmsType_label.setMinimumSize(QSize(0, 30))
        self.pelmsType_label.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.pelmsType_label.setFont(font)
        self.pelmsType_label.setText("")
        self.pelmsType_label.setAlignment(Qt.AlignCenter)
        self.pelmsType_label.setObjectName("pelmsType_label")
        self.verticalLayout_3.addWidget(self.pelmsType_label)
        self.qtdReader_label = QLabel(self.groupBox_Labels)
        self.qtdReader_label.setMinimumSize(QSize(0, 20))
        self.qtdReader_label.setText("")
        self.qtdReader_label.setObjectName("qtdReader_label")
        self.verticalLayout_3.addWidget(self.qtdReader_label)
        self.readerList_label = QLabel(self.groupBox_Labels)
        self.readerList_label.setObjectName("readerList_label")
        self.verticalLayout_3.addWidget(self.readerList_label)
        self.exception_label = QLabel(self.groupBox_Labels)
        self.exception_label.setMinimumSize(QSize(0, 20))
        self.exception_label.setText("")
        self.exception_label.setObjectName("exception_label")
        self.verticalLayout_3.addWidget(self.exception_label)
        self.reader_label = QLabel(self.groupBox_Labels)
        self.reader_label.setMinimumSize(QSize(0, 20))
        self.reader_label.setText("")
        self.reader_label.setObjectName("reader_label")
        self.verticalLayout_3.addWidget(self.reader_label)
        self.id_label = QLabel(self.groupBox_Labels)
        self.id_label.setMinimumSize(QSize(0, 20))
        self.id_label.setText("")
        self.id_label.setObjectName("id_label")
        self.verticalLayout_3.addWidget(self.id_label)
        self.places_label = QLabel(self.groupBox_Labels)
        self.places_label.setMinimumSize(QSize(0, 20))
        self.places_label.setMaximumSize(QSize(16777215, 16777215))
        self.places_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.places_label.setObjectName("places_label")
        self.verticalLayout_3.addWidget(self.places_label)
        self.transitions_label = QLabel(self.groupBox_Labels)
        self.transitions_label.setMinimumSize(QSize(0, 20))
        self.transitions_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.transitions_label.setObjectName("transitions_label")
        self.verticalLayout_3.addWidget(self.transitions_label)
        self.verticalLayout_15.addWidget(self.groupBox_Labels)
        self.horizontalLayout.addLayout(self.verticalLayout_15)
        self.markingGroupBox2 = QGroupBox(self.tab_petrinet)
        self.markingGroupBox2.setMinimumSize(QSize(100, 0))
        self.markingGroupBox2.setMaximumSize(QSize(130, 16777215))
        self.markingGroupBox2.setTitle("")
        self.markingGroupBox2.setObjectName("markingGroupBox2")
        self.verticalLayout_13 = QVBoxLayout(self.markingGroupBox2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_9 = QLabel(self.markingGroupBox2)
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_13.addWidget(self.label_9)
        self.markingVector2_tw = QTableWidget(self.markingGroupBox2)
        self.markingVector2_tw.setMaximumSize(QSize(120, 16777215))
        self.markingVector2_tw.setObjectName("markingVector2_tw")
        self.markingVector2_tw.setColumnCount(0)
        self.markingVector2_tw.setRowCount(0)
        self.markingVector2_tw.horizontalHeader().setDefaultSectionSize(30)
        self.markingVector2_tw.horizontalHeader().setMinimumSectionSize(30)
        self.markingVector2_tw.horizontalHeader().setStretchLastSection(True)
        self.markingVector2_tw.verticalHeader().setMinimumSectionSize(30)
        self.verticalLayout_13.addWidget(self.markingVector2_tw)
        self.horizontalLayout.addWidget(self.markingGroupBox2)
        self.groupBoxMatrix2 = QGroupBox(self.tab_petrinet)
        self.groupBoxMatrix2.setMinimumSize(QSize(350, 0))
        self.groupBoxMatrix2.setTitle("")
        self.groupBoxMatrix2.setObjectName("groupBoxMatrix2")
        self.verticalLayout_14 = QVBoxLayout(self.groupBoxMatrix2)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_10 = QLabel(self.groupBoxMatrix2)
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_14.addWidget(self.label_10)
        self.incMatrix2_tw = QTableWidget(self.groupBoxMatrix2)
        self.incMatrix2_tw.setMinimumSize(QSize(250, 0))
        self.incMatrix2_tw.setObjectName("incMatrix2_tw")
        self.incMatrix2_tw.setColumnCount(0)
        self.incMatrix2_tw.setRowCount(0)
        self.incMatrix2_tw.horizontalHeader().setDefaultSectionSize(30)
        self.incMatrix2_tw.horizontalHeader().setMinimumSectionSize(30)
        self.incMatrix2_tw.horizontalHeader().setStretchLastSection(True)
        self.incMatrix2_tw.verticalHeader().setMinimumSectionSize(30)
        self.verticalLayout_14.addWidget(self.incMatrix2_tw)
        self.horizontalLayout.addWidget(self.groupBoxMatrix2)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.runtimeTerminal_label = QLabel(self.tab_petrinet)
        self.runtimeTerminal_label.setEnabled(True)
        self.runtimeTerminal_label.setMinimumSize(QSize(0, 50))
        self.runtimeTerminal_label.setMaximumSize(QSize(16777215, 55))
        palette = QPalette()
        brush = QBrush(QColor(60, 167, 61))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush)
        brush = QBrush(QColor(127, 127, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush)
        brush = QBrush(QColor(170, 170, 170))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush)
        brush = QBrush(QColor(60, 167, 61))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        brush = QBrush(QColor(60, 167, 61))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush = QBrush(QColor(60, 167, 61))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush)
        brush = QBrush(QColor(127, 127, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush)
        brush = QBrush(QColor(170, 170, 170))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush)
        brush = QBrush(QColor(60, 167, 61))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        brush = QBrush(QColor(60, 167, 61))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        brush = QBrush(QColor(127, 127, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush)
        brush = QBrush(QColor(127, 127, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush)
        brush = QBrush(QColor(170, 170, 170))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush)
        brush = QBrush(QColor(127, 127, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        brush = QBrush(QColor(127, 127, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        self.runtimeTerminal_label.setPalette(palette)
        self.runtimeTerminal_label.setMouseTracking(True)
        self.runtimeTerminal_label.setAutoFillBackground(False)
        self.runtimeTerminal_label.setFrameShape(QFrame.StyledPanel)
        self.runtimeTerminal_label.setFrameShadow(QFrame.Sunken)
        self.runtimeTerminal_label.setText("")
        self.runtimeTerminal_label.setObjectName("runtimeTerminal_label")
        self.verticalLayout_10.addWidget(self.runtimeTerminal_label)
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.transferPNRDSetup_pushButton = QPushButton(self.tab_petrinet)
        self.transferPNRDSetup_pushButton.setObjectName("transferPNRDSetup_pushButton")
        self.verticalLayout_12.addWidget(self.transferPNRDSetup_pushButton)
        self.getRuntimeInfo_pushButton = QPushButton(self.tab_petrinet)
        self.getRuntimeInfo_pushButton.setMinimumSize(QSize(0, 30))
        self.getRuntimeInfo_pushButton.setMaximumSize(QSize(9999999, 16777215))
        self.getRuntimeInfo_pushButton.setObjectName("getRuntimeInfo_pushButton")
        self.verticalLayout_12.addWidget(self.getRuntimeInfo_pushButton)
        self.generateNewPNML_pushButton = QPushButton(self.tab_petrinet)
        self.generateNewPNML_pushButton.setObjectName("generateNewPNML_pushButton")
        self.verticalLayout_12.addWidget(self.generateNewPNML_pushButton)
        self.verticalLayout_10.addLayout(self.verticalLayout_12)
        self.setup_tabWidget.addTab(self.tab_petrinet, "")
        self.verticalLayout_11.addWidget(self.setup_tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 931, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionopen_pnml = QAction(MainWindow)
        icon = QIcon()
        icon.addPixmap(QPixmap(resource_path("images/xml.svg")), QIcon.Normal, QIcon.Off)
        self.actionopen_pnml.setIcon(icon)
        self.actionopen_pnml.setObjectName("actionopen_pnml")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen_Setup_File_pelms = QAction(MainWindow)
        self.actionOpen_Setup_File_pelms.setObjectName("actionOpen_Setup_File_pelms")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionopen_pnml)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_Setup_File_pelms)
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.setup_tabWidget.setCurrentIndex(0)
        self.actionExit.triggered.connect(self.closeEvent)
        QMetaObject.connectSlotsByName(MainWindow)

    def closeEvent(self, event):
      msgBox = QMessageBox()
      msgBox.setIcon(QMessageBox.Icon.Question)
      msgBox.setText("Are you sure you want to close the aplication?")
      msgBox.setWindowTitle("Confirmation")
      msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
      reply = msgBox.exec()
      #reply = QMessageBox.question('Confirmation', 'Are you sure you want to close the aplication?', [QMessageBox.Yes | QMessageBox.No], QMessageBox.No)

      if reply == QMessageBox.Yes:
          if not type(event) == bool:
              event.accept()
          else:
              sys.exit()
      else:
          if not type(event) == bool:
              event.ignore()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate

        #--------------------------------- Window Title Text ---------------------------------
        MainWindow.setWindowTitle(_translate("MainWindow", "PELMS-MQTT"))

        #--------------------------------- Setup Tab Text ---------------------------------
        self.label_6.setText(_translate("MainWindow", "Setup PNRD\n Type"))
        self.setupPelms_comboBox.setItemText(0, _translate("MainWindow", "PNRD"))
        self.setupPelms_comboBox.setItemText(1, _translate("MainWindow", "iPNRD"))
        self.label_7.setText(_translate("MainWindow", "Reader Name: "))
        self.label_8.setText(_translate("MainWindow", "Number of Antennas"))
        self.label_3.setText(_translate("MainWindow", "Platform IP"))
        self.IP_lineEdit.setInputMask(_translate("MainWindow", "000.000.000.000;_"))
        self.IP_lineEdit.setText(_translate("MainWindow", "..."))
        self.addIP_pushButton.setText(_translate("MainWindow", "Add"))
        self.createSetup_pushButton.setText(_translate("MainWindow", "CREATE SETUP FILE"))
        self.marking_vector.setText(_translate("MainWindow", "Marking Vector"))
        self.label.setText(_translate("MainWindow", "Incidence Matrix"))
        self.label_4.setText(_translate("MainWindow", "Incidence Matrix Transpose Array"))
        self.label_2.setText(_translate("MainWindow", "Marking Array"))
        self.setup_tabWidget.setTabText(self.setup_tabWidget.indexOf(self.tab_setup), _translate("MainWindow", "SETUP"))

        #---------------------------------  ---------------------------------
        self.setupInfo_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.readerList_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.places_label.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.transitions_label.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))

        #--------------------------------- Runtime Tab Text ---------------------------------
        self.label_9.setText(_translate("MainWindow", "Marking Vector"))
        self.label_10.setText(_translate("MainWindow", "Incidence Matrix"))
        self.transferPNRDSetup_pushButton.setText(_translate("MainWindow", "TRANSFER PNRD SETUP"))
        self.getRuntimeInfo_pushButton.setText(_translate("MainWindow", "GET RUNTIME INFO"))
        self.generateNewPNML_pushButton.setText(_translate("MainWindow", "TRANSFER INITIAL DATA"))
        self.setup_tabWidget.setTabText(self.setup_tabWidget.indexOf(self.tab_petrinet), _translate("MainWindow", "RUNTIME"))

        #--------------------------------- File Menu Text ---------------------------------
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionopen_pnml.setText(_translate("MainWindow", "Open PNML file"))
        self.actionopen_pnml.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionOpen_Setup_File_pelms.setText(_translate("MainWindow", "Open Setup File (*.pelms)"))
        self.actionOpen_Setup_File_pelms.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+X"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())