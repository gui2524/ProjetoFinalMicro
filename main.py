import RPi.GPIO as gpio
import time
from time import sleep
import log
import sensors
import img_compare
import notification
import app
from threading import Thread

"""-------------GLOBAL VARIABLES------------"""


"""-------------FUNCTIONS------------"""
def notifySensor(comodo, imagePath):
    notification.sendMessage("Comodo: " + str(comodo) + " sob invasao")
    notification.sendPhoto(imagePath)
    log.eventLog("Notificacao enviada")

def main():
    gpio.setmode(gpio.BCM)
    sensors.redefinir_banco()
    thread = Thread(target=checkRooms)
    thread.start()
    app.runApp()

def checkRooms():
    while(True):
        comodosAtivados = sensors.verifica()
        if comodosAtivados != []:
            for el in comodosAtivados:
                log.eventLog("Comodo: " + str(el) + " sob invasao")
                cameraId = el.getCameraId()
                log.log(el.getCameraId())
                imagePath = img_compare.takePhoto(cameraId)
                notifySensor(el, imagePath)


"""-------------EXEC------------"""
main()
