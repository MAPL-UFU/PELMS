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

import os

class FileCreator:
    def __init__(self, dir_name, pathName, fileName, extension, flagPrint = False):
        self.location = pathName + f'/{dir_name}'
        self.fileName = fileName
        self.extension = extension
        self.flag = flagPrint
        self.create_dir(self.location)

    def set_text(self,txt):
        f= open(f'{self.location}/{self.fileName}.{self.extension}',"w+")
        f.write(txt)
        f.close()
        print(f'Arquivo {self.location}/{self.fileName}.{self.extension} criado com sucesso') if self.flag else None

    def set_text_increment(self,txt):
        text = ''

        if self.verify_if_file(f'{self.location}/{self.fileName}.{self.extension}'):
            f=open(f'{self.location}/{self.fileName}.{self.extension}', "a")
            text = f'Arquivo {self.location}/{self.fileName}.{self.extension} editado com sucesso'
        else:
            f= open(f'{self.location}/{self.fileName}.{self.extension}',"w+")
            text = f'Arquivo {self.location}/{self.fileName}.{self.extension} criado com sucesso'

        f.write(txt)
        f.close()

        print(text) if self.flag else None

    def create_dir(self, dirname):
        if  os.path.isdir(dirname):
            print (f'Diretório  {dirname} já criado')  if self.flag else None
        else:
            try:
                os.makedirs(dirname)
            except OSError:
                print(f'A criação do Diretório {dirname} Falhou') if self.flag else None
            else:
                print(f'Diretório {dirname} criado com sucesso') if self.flag else None

    def verify_if_file(self,fileName):
        if  os.path.isfile(fileName) :
            return True
        else :
            return False