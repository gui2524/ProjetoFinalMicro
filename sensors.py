from gpiozero import Button, MotionSensor, DistanceSensor
from time import sleep
#from pymongo import *
from json import load
import os
import RPi.GPIO as GPIO
import log

"""-------------GLOBAL VARIABLES------------"""

global_diretorio_atual = os.path.dirname(os.path.abspath(__file__))
SALAS_FILE = 'salas.json'
SALAS_PATH = global_diretorio_atual + '/' + SALAS_FILE
global_listaComodos = []



"""-------------FUNCTIONS------------"""

class Comodo:
    def __init__(self, nome, sensorSom, tracker, sensorPresenca, sensorDistancia):
        self.nome = nome
        self.sensorSom = sensorSom
        self.tracker = tracker
        self.sensorPresenca = sensorPresenca
        self.sensorDistancia = sensorDistancia
    
    def __str__(self):
        return self.nome
        
def ativa_sensor(comodo,sensor):
    log.log("presenca detectada: " + comodo)
    log.log("Sensor ativado: " + sensor)

def ativa():
    log.log("presenca detectada: ")

def movimento1():
    presenca.when_motion = ativa
    #presenca.when_no_motion = print(" Parou!")
    print ("detector de movimento ativo")

def redefinir_banco():
    log.eventLog("Redefinindo arquivo de configuracao da sala")

    salasFile = open(SALAS_PATH)
    dados = load(salasFile)
    salasFile.close()

    for i in dados:
        comodo = Comodo(i.get("nome"), i.get("sensor_de_som"), i.get("tracker"), i.get("sensor_presenca"), i.get("sensor_distancia"))
        global_listaComodos.append(comodo)
        log.eventLog("Comodo: " + comodo.nome + "\n Sensor de som: " + str(comodo.sensorSom) + "\n Sensor de Presenca: " + str(comodo.sensorPresenca)
                     + "\n Sensor de tracker: " + str(comodo.tracker) + "\n Sensor de Distancia: " + str(comodo.sensorDistancia))

def verifica():

    for comodo in global_listaComodos:

        if (comodo.tracker is not None):
            s_tracker = comodo.tracker
            track = Button(s_tracker)
            if (track.is_pressed == True):
                local_casa = comodo.nome
                sensor_comodo = "Tracker"
                ativa_sensor(local_casa, sensor_comodo)
                
        if (comodo.sensorSom is not None):
            s_som = comodo.sensorSom
            som = Button(s_som)
            if (som.is_pressed == True):
                local_casa = comodo.nome
                sensor_comodo = "Sensor de Som"
                ativa_sensor(local_casa, sensor_comodo)
                
        if (comodo.sensorPresenca is not None):
            s_presenca = comodo.sensorPresenca
            global presenca
            presenca=MotionSensor(s_presenca)
            if (presenca.when_motion == True):
                presenca.when_motion = ativa
#                local_casa=comodo.nome
#                sensor_comodo= "Sensor de Presenca"
#                presenca.when_motion=ativa_sensor(local_casa,sensor_comodo)
#                presenca.when_no_motion=print("Sem movimento")
#                print("antes do movimento1")
#                presenca.when_motion=movimento1
            
            
               
#        if (comodo.sensorSom is not None):
#            print("Sensor de som: " + str(comodo.sensorSom))
#        if (comodo.sensorPresenca != None):
#            print("Sensor de Presenca: " + str(comodo.sensorPresenca))
          
#        if (track.is_pressed == True):
#            print(comodo.nome)            
#            print("Sensor de tracker: " + str(comodo.tracker))
#        if (comodo.sensorDistancia is not None):
#            s_trigger=comodo.sensorDistancia[0]
#            s_echo=comodo.sensorDistancia[1]
#            distance=DistanceSensor(trigger=s_trigger, echo=s_echo)
#            ds=distance.distance
#            print(ds)
#            if(distance.when_in_range==True):
#            if(ds<0.05):
#                local_casa=comodo.nome
#                sensor_comodo= "Sensor de Distancia"
#                ativa_sensor(local_casa,sensor_comodo)
                

"""-------------TEST------------"""

#track= Button()
#sensor= DistanceSensor(trigger=4,echo=18)

#sensor.wait_for_in_range()
#sensor.wait_for_out_of_range()
#sensor.threshold_distance=0.5
#c="ok"


#def alerta():
    #print('Alguem entrou no quarto')
    #d = sensor.distance*100
    #print(str(int (d)) + " cm")
    #sleep(.5)

   
 
# redefinir_banco()
#while True:
    #verifica()
    
#    if (GPIO.input(5)==True)
#        def ativa():
    
#    print(sensor.distance)
#    sensor.when_in_range=ativa_sensor(c)
    
    #sleep(0.1)