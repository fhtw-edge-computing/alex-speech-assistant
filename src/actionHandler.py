import os
import importlib
import requests

speechService = importlib.import_module("speechService")
actionHandlerMap = {}


def init():
	moduleName = 'actions'
	obj = os.scandir(moduleName)
	for entry in obj:
		name = entry.name
		if entry.is_file() and name.endswith('.py') and (not name.startswith('_')):
			handler = importlib.import_module(f'{moduleName}.{name.replace(".py", "")}')
			actionType = None
			if handler and callable(getattr(handler, 'getActionTypes', None)) and callable(getattr(handler, 'doAction', None)):
				actionTypes = handler.getActionTypes()
			if len(actionTypes) > 0:
				for actionType in actionTypes:
					actionHandlerMap[actionType] = handler
			else:
				print(f'WARN: coudn\'t import file "{name}" as action handler!')
			
init()

def doAction(item, text, config):
	if not item or not item["actionType"]:
		print("invalid item!")
		print(item)
		return

	if actionHandlerMap.get(item["actionType"]):
		handler = actionHandlerMap.get(item["actionType"])
		handler.doAction(item, text, item["actionType"], config)
	else:
		print(f'WARN: no action handler found for item {item}')

def stop():
	speechService.stopSpeaking()
	
