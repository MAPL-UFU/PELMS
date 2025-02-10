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

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PopupInfo(QWidget):
    submitted = pyqtSignal([str], [int, str])

    def __init__(self,msg):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.info_label = QLabel()
        self.info_label.setText(msg)
        self.submit = QPushButton('Ok', clicked=self.onSubmit)

        self.layout().addWidget(self.info_label)
        self.layout().addWidget(self.submit)

    def onSubmit(self):
        self.close()