from gpiozero import Button,MotionSensor
from datetime import datetime
from time import strftime
from time import sleep
from json import load
import json
import os
import RPi.GPIO as gpio
import time
import log

"""-------------GLOBAL VARIABLES------------"""

global_diretorio_atual = os.path.dirname(os.path.abspath(__file__))
SALAS_FILE = 'salas.json'
SALAS_PATH = global_diretorio_atual + '/' + SALAS_FILE
global_listaComodos = []
SALAS_VERIFICA_TIME = 30
global_comodosTime = [0, 0, 0, 0, 0]


"""-------------FUNCTIONS------------"""

class Comodo:
    def __init__(self, nome, sensorSom, tracker, sensorPresenca, sensorLuz, pinoPresenca, cameraId):
        self.nome = nome
        self.sensorSom = sensorSom
        self.tracker = tracker
        self.sensorPresenca = sensorPresenca
        self.sensorLuz = sensorLuz
        self.pinoPresenca = pinoPresenca
        self.cameraId = cameraId
    
    def __str__(self):
        return self.nome

    def getCameraId(self):
        return self.cameraId
        
##def ativa_sensor(comodo,sensor):
##    log.log("presenca detectada: " + comodo)
##    log.log("Sensor ativado: " + sensor)
##
##def ativa():
##    log.log("presenca detectada: ")
##
##def movimento1():
##    presenca.when_motion = ativa
##    #presenca.when_no_motion = print(" Parou!")
##    print ("detector de movimento ativo")

def getListaComodos():
    return global_listaComodos

def redefinir_banco():
    log.eventLog("Redefinindo arquivo de configuracao da sala")

    salasFile = open(SALAS_PATH)
    dados = load(salasFile)
    salasFile.close()

    for i in dados:
        nome = i.get("nome")
        sensorSom = i.get("sensor_de_som")
        tracker = i.get("tracker")
        presenca = i.get("sensor_presenca")
        sensorLuz = i.get("sensor_de_luz")
        cameraId = i.get("cameraId")

        log.eventLog("Comodo: " + nome + "\n Sensor de som: " + str(sensorSom) + "\n Sensor de Presenca: " + str(presenca)
                     + "\n Sensor de tracker: " + str(tracker) + "\n Sensor de Luz: " + str(sensorLuz) + "\n Camera ID: " + str(cameraId))

        if tracker is not None:
            trackButton = Button(tracker)
        else:
            trackButton = None

        if (sensorLuz!= None):
            luzButton = Button(sensorLuz)
        else:
            luzButton = None

        if (presenca!= None):
            presencaSensor = MotionSensor(presenca)
            gpio.setup(presenca, gpio.IN, pull_up_down = gpio.PUD_DOWN)
        else:
            presencaSensor = None
    
        comodo = Comodo(nome, sensorSom, trackButton, presencaSensor, luzButton, presenca, cameraId)
        global_listaComodos.append(comodo)
        

def verifica():
    listaComodosAcionados = []
    comodoCounter = 0
    for comodo in global_listaComodos:
        comodoAtivado = False
        currentTime = time.time()
        if(currentTime - global_comodosTime[comodoCounter] > SALAS_VERIFICA_TIME) :
            if (comodo.tracker!= None):
                if (comodo.tracker.is_pressed==True):
                    log.log("Sensor ativado: Tracker // Local: " + comodo.nome)
                    listaComodosAcionados.append(comodo)
                    comodoAtivado = True
            
            if (comodo.sensorLuz!= None):
                if (comodo.sensorLuz.is_pressed==True):
                    log.log("Sensor ativado: Sensor de Luz // Local: " + comodo.nome)
                    listaComodosAcionados.append(comodo)
                    comodoAtivado = True
                    
            if (comodo.sensorPresenca!= None):
                 if(gpio.input(comodo.pinoPresenca)==1):
                    log.log("Sensor ativado: Sensor de Presenca // Local: " + comodo.nome)
                    listaComodosAcionados.append(comodo)
                    comodoAtivado = True

            if comodoAtivado == True:
                global_comodosTime[comodoCounter] = currentTime
           
        comodoCounter += 1

    return listaComodosAcionados
"""-------------TEST------------"""

##gpio.setmode(gpio.BCM)
##
##redefinir_banco()
##
##while True: 
##    verifica() 
##    sleep(.1)
