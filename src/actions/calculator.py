import importlib
from enum import Enum, auto
import numbers
import math

stringUtil = importlib.import_module("stringUtil")
speechService = importlib.import_module("speechService")
util = importlib.import_module("util")

def getActionTypes():
	return ["CALCULATOR"]


class OPERATORS(Enum): 
	MULTIPLY = auto()
	DIVIDE = auto()
	EXPONENTIATE = auto()
	SQUARE = auto()
	LOG = auto()
	SQUAREROOT = auto()
	ADD = auto()
	SUBSTRACT = auto()
	
operatorWordMap = {
	OPERATORS.MULTIPLY: ["mal"],
	OPERATORS.DIVIDE: ["durch"],
	OPERATORS.EXPONENTIATE: ["hoch"],
	OPERATORS.SQUARE: ["quadrat"],
	OPERATORS.LOG: ["logarithmus"],
	OPERATORS.SQUAREROOT: ["wurzel", "wurzeln"],
	OPERATORS.ADD: ["plus", "und"],
	OPERATORS.SUBSTRACT: ["minus", "weniger"]
}

operatorFnMap = {
	OPERATORS.MULTIPLY: lambda x,y: x * y,
	OPERATORS.DIVIDE: lambda x,y: x / y,
	OPERATORS.EXPONENTIATE: lambda x,y: x ** y,
	OPERATORS.SQUARE: lambda x, y: x ** 2,
	OPERATORS.LOG: lambda x, y: math.log(y),
	OPERATORS.SQUAREROOT: lambda x,y: math.sqrt(y),
	OPERATORS.ADD: lambda x,y: x + y,
	OPERATORS.SUBSTRACT: lambda x,y: x - y
}

operatorNumCountMap = {
	OPERATORS.ADD: 2,
	OPERATORS.MULTIPLY: 2,
	OPERATORS.DIVIDE: 2,
	OPERATORS.EXPONENTIATE: 2,
	OPERATORS.SQUARE: 1,
	OPERATORS.LOG: 1,
	OPERATORS.SQUAREROOT: 1,
	OPERATORS.SUBSTRACT: 2
}

operatorNumPosMap = {
	OPERATORS.SQUARE: 0,
	OPERATORS.LOG: 1,
	OPERATORS.SQUAREROOT: 1
}

resultWord = "ergebnis"
lastResult = None

def doAction(item, text, actionType, config):
	global lastResult
	
	operator = getOperator(text)
	if operator:
		operatorWord = getOperatorWord(operator, text)
		parts = text.split(operatorWord, 1)
		numbers = list(map(lambda x: stringUtil.parseNumber(x, config.get("lang")), parts))
		print(parts)
		print(numbers)
		if (not util.isNumber(numbers[0])) and resultWord in parts[0]:
			numbers[0] = lastResult
		if (not util.isNumber(numbers[1])) and resultWord in parts[1]:
			numbers[1] = lastResult
		
		result = None
		if operatorNumCountMap.get(operator) == 2 and util.isNumber(numbers[0]) and util.isNumber(numbers[1]):
			result = operatorFnMap.get(operator)(numbers[0], numbers[1])
			text = f'{round(numbers[0], 3)} {operatorWordMap.get(operator)[0]} {round(numbers[1], 3)} ist {round(result, 3)}'
		elif operatorNumCountMap.get(operator) == 1:
			result = operatorFnMap.get(operator)(numbers[0], numbers[1])
			if operatorNumPosMap.get(operator) == 0:
				text = f'{round(numbers[0], 3)} {operatorWordMap.get(operator)[0]} ist {round(result, 3)}'
			else:
				text = f'{operatorWordMap.get(operator)[0]} {round(numbers[1], 3)} ist {round(result, 3)}'
		
		if not result:
			text = "Tut mir leid, das kann ich nicht rechnen"
		else:
			lastResult = result
		speechService.speak(text)
	else:
		speechService.speak("War das eine Rechnung? Ich habe sie nicht verstanden")
		
	
		
def getOperator(text):
	for operator in OPERATORS:
		if stringUtil.anyWordExists(text, operatorWordMap.get(operator)):
			return operator
			
def getOperatorWord(operator, text):
	words = operatorWordMap.get(operator)
	for word in words:
		if word in text:
			return word
