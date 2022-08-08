import requests
from lxml import html
import importlib
speechService = importlib.import_module("speechService")
util = importlib.import_module("util")

def getActionTypes():
	return ["EXTRACT_WEBSITE"]


def doAction(item, text, actionType, config):
	if not util.validAttributes(item, ["url"]):
		return
		
	text = extractFromWebsite(item.get("url"), item.get("xpath"))
	fallback = item.get("fallback") if item.get("fallback") else "Ich konnte die Website nicht abrufen"
	text = text if text else fallback
	speechService.speak(text)
		
def extractFromWebsite(url, xpath):
	try:
		content = requests.get(url).content
		tree = html.fromstring(content)
		xpathSelector = xpath if xpath else "//body//text()"
		return " ".join(tree.xpath(xpathSelector)).replace("'", "").replace('"', '')
	except:
		return None
