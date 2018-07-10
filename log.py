from datetime import datetime
import os

"""-------------GLOBAL VARIABLES------------"""
TIME_FORMAT = "%H:%M:%S"
global_diretorio_atual = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = global_diretorio_atual + "/log/log.txt"

"""-------------FUNCTIONS------------"""

def formatText(text):
    time = datetime.now()
    timeFormatted = time.strftime(TIME_FORMAT)
    textFormatted = timeFormatted + " ---> " + str(text) + "\n"
    return textFormatted

def log(text):
    logText = formatText(text)
    print(logText)

def eventLog(text):
    logText = formatText(text)
    log(text)
    with open(LOG_PATH, "a") as textFile:
        textFile.write(logText)


"""-------------TEST------------"""
##eventLog("TesteA")
# log("TesteB")
