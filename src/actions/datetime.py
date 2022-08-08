import time
from datetime import datetime
import locale
import importlib
speechService = importlib.import_module("speechService")

def getActionTypes():
	return ["CURRENT_TIME", "CURRENT_DATE"]

def doAction(item, text, actionType, config):
	locale.setlocale(locale.LC_ALL, '') # to use current system locale
	
	if actionType == "CURRENT_TIME":
		unixTime = getUnixTime()
		if not unixTime:
			speechService.speak("Ich kann die Uhrzeit nicht abrufen")
		else:
			speechService.speak(f'Es ist {getTimeReadable(unixTime)} Uhr')
				
	elif actionType == "CURRENT_DATE":
		unixTime = getUnixTime()
		if not unixTime:
			speechService.speak("Ich kann das Datum nicht abrufen")
		else:
			speechService.speak(f'Heute ist {getDateReadable(unixTime)}')
			
def getUnixTime():
	return time.time()
					
def getUnixTimeOnline():
	unixTime = None
	try:
		return int(requests.get("https://time.asterics-foundation.org/").content)
	except:
		return None

def getTimeReadable(unixTime):
	return datetime.fromtimestamp(unixTime).strftime("%H:%M")
	
def getDateReadable(unixTime):
	return datetime.fromtimestamp(unixTime).strftime("%A, %d. %B %Y")
