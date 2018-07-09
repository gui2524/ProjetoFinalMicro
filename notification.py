from requests import *
from urllib.request import urlretrieve

"""-------------GLOBAL VARIABLES------------"""

global_key = "COLOQUE A SUA CHAVE AQUI!"
global_chatId = "COLOQUE O ID DA SUA CONVERSA AQUI!"
global_baseAddress = "https://api.telegram.org/bot" + global_key
global_nextUpdateId = 0


"""-------------FUNCTIONS------------"""

def sendMessage(message):
	address = global_baseAddress + "/sendMessage"
	data = {"chat_id": global_chatId, "text": message}
	response = post(address, data=data)
	print(response)

def sendPhoto(imagePath):
	address = global_baseAddress + "/sendPhoto"
	data = {"chat_id": global_chatId}
	photoFile = {"photo": open("foto.jpeg", "rb")}
	response = post(address, data=data, files=photoFile)
	print(response)

def getUpdates():
	address = global_baseAddress + "/getUpdates"
	data = {"offset": global_nextUpdateId}
	response = get(address, json=data)
	print(response)
	
	if(response == None):
		return None
	
    responseDict = response.json()


    for result in responseDict["result"]:
        message = result["message"]
		if "text" in message:
			text = message["text"]
		elif "voice" in message:
			fileId = message["voice"]["file_id"]
		elif "photo" in message:
			photo = message["photo"][-1]
			photoId = photo["file_id"]
			
	global_nextUpdateId = int(result["update_id"]) + 1
	
def getFile(fileId, fileName):
	address = global_baseAddress + "/getFile"
	data = {"file_id": fileId}
	response = get(endereco, json=data)
	print(response)
	
	if(response == null):
		return null
		
	responseDict = response.json()
	filePath = responseDict["result"]["file_path"]

	fileAddress = "https://api.telegram.org/file/bot" + global_key + "/" + filePath
	urlretrieve(fileAddress, fileName)
	
	
"""-------------TEST------------"""
