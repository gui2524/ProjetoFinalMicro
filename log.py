from datetime import datetime

"""-------------GLOBAL VARIABLES------------"""
LOG_FILE = "log.txt"
TIME_FORMAT = "%H:%M:%S"


"""-------------FUNCTIONS------------"""

def formatText(text):
    time = datetime.now()
    timeFormatted = time.strftime(TIME_FORMAT)
    textFormatted = timeFormatted + " ---> " + text + "\n"
    return textFormatted

def log(text):
    logText = formatText(text)
    print(logText)

def eventLog(text):
    logText = formatText(text)
    log(text)
    with open(LOG_FILE, "a") as textFile:
        textFile.write(logText)


"""-------------TEST------------"""
# eventLog("TesteA")
# log("TesteB")
