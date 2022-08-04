import requests
import time
from datetime import datetime
from lxml import html
import random
import importlib

speechService = importlib.import_module("speechService")
openHab = importlib.import_module("openHabConnector")
actionCalculator = importlib.import_module("actionCalculator")

def doAction(item, text):
	if not item or not item["actionType"]:
		print("invalid item!")
		return
	
	actionType = item["actionType"]
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
			speechService.speak(f'Heute ist der {getDateReadable(unixTime)}')
			
	elif actionType == "TELL_JOKE":
		playTextWithFallback(getJoke(), "Ich habe keinen Witz gefunden")
			
	elif actionType == "TELL_WEATHER":
		playTextWithFallback(getWeather(), "Ich kann das Wetter nicht abrufen")
		
	elif actionType == "ANSWER_CUSTOM":
		speechService.speak(random.choice(item["answers"]))
	
	elif actionType == "OPENHAB":
		openHab.doAction(item, text)
		
	elif actionType == "CALCULATOR":
		actionCalculator.doAction(item, text)

def stop():
	speechService.stopSpeaking()

def playTextWithFallback(text, fallback):
	if not text:
		speechService.speak(fallback)
	else:
		speechService.speak(text)

def getJoke():
	try:
		content = requests.get("https://witze.net/zuf%C3%A4llige-witze").content
		tree = html.fromstring(content)
		return " ".join(tree.xpath('(//div[@class="joke"])[1]/text()')).replace("'", "").replace('"', '')
	except:
		return None
		
def getWeather():
	try:
		content = requests.get("https://wetter.orf.at/wien/").content
		tree = html.fromstring(content)
		return " ".join(tree.xpath('(//p[@class="teaser"])[1]/text()')).replace("'", "").replace('"', '')
	except:
		return None

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
	return datetime.fromtimestamp(unixTime).strftime("%d. %B %Y")
	
