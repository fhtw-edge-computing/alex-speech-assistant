import random
import importlib
speechService = importlib.import_module("speechService")
util = importlib.import_module("util")

def getActionTypes():
	return ["ANSWER_CUSTOM"]


def doAction(item, text, actionType, config):
	if not util.validAttributes(item, ["answers"]):
		return
		
	speechService.speak(random.choice(item["answers"]))
