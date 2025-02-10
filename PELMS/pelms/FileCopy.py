'''
Created on Jan, 2025
@author: Álisson Carvalho Vasconcelos
@Github authors: AlissonCV
'''

import os
import shutil

class FileCopy:
    def __init__(self, paste_path, copy_path, copy_file_name, paste_file_name, file_extension, flagPrint = False):
        self.copy_path = copy_path
        self.paste_path = paste_path
        self.copy_file_name = f'{copy_file_name}.{file_extension}'
        self.paste_file_name = f'{paste_file_name}.{file_extension}'
        self.extension = file_extension
        self.flag = flagPrint
        self.create_dir(self.paste_path)

    def copy_file(self):
        text = ''

        if self.paste_path != self.copy_path:
            shutil.copy(
                f'{self.copy_path}/{self.copy_file_name}',
                f'{self.paste_path}/{self.paste_file_name}'
            )

            text = f'Arquivo {self.copy_file_name} copiado com sucesso para {self.paste_path}'
        else:
            text = f'Arquivo já se encotra em {self.paste_path}'

        print(text) if self.flag else None

    def move_file(self):
        text = ''

        if self.paste_path != self.copy_path:
            shutil.move(
                f'{self.paste_path}.{self.extension}',
                f'{self.paste_path}/{self.paste_file_name}'
            )

            text = f'Arquivo {self.copy_file_name} movido com sucesso para {self.paste_path}/{self.paste_file_name}'
        else:
            text = f'Arquivo já se encotra em {self.paste_path}/{self.paste_file_name}'

        print(text) if self.flag else None

    def create_dir(self, dirname):
        if  os.path.isdir(dirname):
            print (f'Diretório  {dirname} já criado')  if self.flag else None
        else:
            try:
                os.makedirs(dirname)
            except OSError:
                print (f'A criação do Diretório  {dirname} Falhou')  if self.flag else None
            else:
                print (f'Diretório  {dirname} criado com sucesso')  if self.flag else None