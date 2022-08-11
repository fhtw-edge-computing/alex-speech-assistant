import requests
from lxml import html
import urllib.parse
import importlib
speechService = importlib.import_module("speechService")
util = importlib.import_module("util")

def getActionTypes():
	return ["EXTRACT_WEBSITE"]


def doAction(item, text, actionType, config):
	if not util.validAttributes(item, ["url"]):
		return None
		
	return getActionText(item.get("url"), item.get("xpath"), item.get("fallback"))
	
def getActionText(url, xpath, fallback=None, urlargs=[]):
	if (not url):
		return None
	text = extractFromWebsite(url, xpath, urlargs)
	fallback = fallback if fallback else "Ich konnte die Website nicht abrufen"
	text = text if text else fallback
	return text
		
def extractFromWebsite(url, xpath, urlargs=[]):
	try:
		url = urllib.parse.unquote(url)
		print(url)
		print(urlargs)
		url = url.format(*urlargs)
		print(url)
		xpathSelector = urllib.parse.unquote(xpath) if xpath else "//body//text()"
		content = requests.get(urllib.parse.unquote(url)).content
		tree = html.fromstring(content)
		return " ".join(tree.xpath(xpathSelector)).replace("'", "").replace('"', '')
	except:
		return None
