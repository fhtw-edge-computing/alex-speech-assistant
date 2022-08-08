import numbers

def isNumber(value):
	return isinstance(value, numbers.Number)
	
def validAttributes(jsonObject, neededAttributeNames):
	missing = []
	for attribute in neededAttributeNames:
		if attribute not in jsonObject:
			missing.append(attribute)
	
	if len(missing) > 0:
		print(f'WARN: json item {jsonObject} has missing attributes {missing}')
		return False
	return True
