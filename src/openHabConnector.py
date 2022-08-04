import requests
import importlib

stringUtil = importlib.import_module("stringUtil")

def doAction(item, text):
	data = extractOpenHabData(item, text)
	print(f'post {data} to {item["url"]}')
	try:
		requests.post(item["url"], data=data)
	except:
		print("request to openHAB failed")

def extractOpenHabData(item, text):
	data = stringUtil.parseNumber(text)
	if data:
		return data
	
	paramType = item.get("paramType")
	if stringUtil.anyExists(text, ["aus", "ausschalten", "abschalten", "abdrehen"], padWhitespace=True):
		data = "OFF" if paramType != "number" else 0
	elif stringUtil.anyExists(text, ["ein", "einschalten", "aufdrehen"], padWhitespace=True):
		data = "ON" if paramType != "number" else 100
	elif stringUtil.anyExists(text, ["stopp", "stoppen", "halt"], padWhitespace=True):
		data = "STOP"
	elif stringUtil.anyExists(text, ["auf", "aufmachen", "oben", "rauf"], padWhitespace=True):
		data = "UP"
	elif stringUtil.anyExists(text, ["zu", "zumachen", "unten", "runter"], padWhitespace=True):
		data = "DOWN"
		
	return data
