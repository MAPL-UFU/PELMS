'''
Created on Nov, 2021
Updated on:
  * Jan, 2022
  * Jan, 2025
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

def template_mqtt(tagid, reader, error, antenna, fire, date, time):
    return f'\
Tag Id: {tagid}\n\
Reader: {reader}\n\
Error: {error}\n\
Antenna: {antenna}\n\
Fire Position: {fire}\n\
Date: {date}\n\
Time: {time}\n\
\n\n'

def template_pnrd_data(n_places, n_transitions, IncidenceMatrix, StartingTokenVector, FireVector):
    text_format = f'place: {n_places}\ntransition: {n_transitions}\ntoken: {{{StartingTokenVector}}}\nincidence: {{{IncidenceMatrix}}}'

    if FireVector == None:
        text_format += f'\nfire: {{{FireVector}}}'

    return text_format

def template_recorder(pelmsType, topic):
    pelmsType = pelmsType.lower()
    pathName = f'{os.getcwd()}/pelms/utils'
    finalText = ''

    with open(f'{pathName}/template_begin.ino', "r") as begin:
        with open(f'{pathName}/template_recorder_{pelmsType}.ino') as pnrd:
            for text in begin:
                finalText += text
            finalText += "\n\n"
            for text in pnrd:
                finalText += text

    if pelmsType == 'pnrd':
        pnrd_dict = {
            'place': 1,
            'transition': 2,
            'token': 3,
            'incidence': 4
        }
    else:
        pnrd_dict = {
            'place': 1,
            'transition': 2,
            'fire': 3
        }

    for i in pnrd_dict.keys():
        finalText = finalText.replace(f'PELMSVAR{pnrd_dict[i]}', topic[i])

    return finalText

def template_reader(pelmsType, topic):
    pelmsType = pelmsType.lower()
    pathName = f'{os.getcwd()}/pelms/utils'
    finalText = ''

    with open(f'{pathName}/template_begin.ino', "r") as begin:
        with open(f'{pathName}/template_reader_{pelmsType}.ino') as pnrd:
            for text in begin:
                finalText += text
            finalText += "\n\n"
            for text in pnrd:
                finalText += text

    if pelmsType == 'pnrd':
        pnrd_dict = {
            'place': 1,
            'transition': 2,
            'runtime': 3
        }
    else:
        pnrd_dict = {
            'place': 1,
            'transition': 2,
            'incidence': 3,
            'token': 4,
            'runtime': 5
        }

    runtime_dict = {
        'id': 0,
        'reader': 1,
        'error': 2,
        'antenna': 3,
        'fire': 4
    }

    for i in pnrd_dict.keys():
        if i == 'runtime':
            for j in runtime_dict.keys():
                finalText = finalText.replace(f'PELMSVAR{pnrd_dict[i]+runtime_dict[j]}', f'{topic[i]}{j}')
        else:
            topic_array = topic[i].split('/')
            finalText = finalText.replace(f'PELMSVAR{pnrd_dict[i]}', topic[i].replace(topic_array[-1], f'fire/{topic_array[-1]}'))

    return finalText

def template_recorder_h(ssid, passWord, clientid, server, port, serial, topic, userName=None, anonymous=None):
    return template_wifi_h(ssid, userName, passWord, anonymous, clientid, server, port, serial, topic)

def template_reader_h(ssid, passWord, clientid, server, port, serial, topic, reader, antennaid, position, userName=None, anonymous=None):
    return template_wifi_h(ssid, userName, passWord, anonymous, clientid, server, port, serial, topic, reader, antennaid, position)

def template_wifi_h(ssid, userName, passWord, anonymous, clientid, server, port, serial, topic, readerid=None, antennaid=None, position=None):
    pathName = f'{os.getcwd()}/pelms/utils'
    finalText = ''

    pelms_dict = {
        'ssid': ssid,
        'userwame': 'XXXX' if userName == None else userName,
        'password': passWord,
        'anonymous': 'anonymous@ufu.br' if anonymous == None else anonymous,
        'clientid': clientid,
        'server': server,
        'port': port,
        'serial': serial,
        'topic': topic,
        'readerid': readerid,
        'antennaid': antennaid,
        'position': position
    }

    with open(f'{pathName}/template_wifipassword.h', "r") as file:
        for text in file:
            finalText += text

    if pelms_dict['readerid'] != None:
        finalText = f'{finalText}\n\n/* DECLARATION OF FILE VARIABLES */\nString pelmsReader = \"PELMSVAR10\";\nString pelmsAntenna = \"PELMSVAR11\";\nString pelmsPosition = \"PELMSVAR12\";'

    j = 0
    for i in pelms_dict.keys():
        j += 1
        if j < 10:
            finalText = finalText.replace(f'PELMSVAR0{j}', f'{pelms_dict[i]}')
        else:
            finalText = finalText.replace(f'PELMSVAR{j}', f'{pelms_dict[i]}')

    return finalText