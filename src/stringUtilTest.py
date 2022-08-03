import importlib
stringUtil = importlib.import_module("stringUtil")

def assertEqual(value1, value2):
	if value1 != value2:
		print (f'Error: "{value1}" is not equal to "{value2}"')

print("test stringUtil.prepareWordForNumConversion()")
assertEqual(stringUtil.prepareWordForNumConversion("einundzwanzig"), "eins und zwanzig")
assertEqual(stringUtil.prepareWordForNumConversion("hundertzwei"), "hundert zwei")
assertEqual(stringUtil.prepareWordForNumConversion("einhundertdreiunddreißig"), "ein hundert drei und dreizig")
assertEqual(stringUtil.prepareWordForNumConversion("zweitausend vierhundert vierundvierzig"), "zwei tausend vier hundert vier und vierzig")
assertEqual(stringUtil.prepareWordForNumConversion("hallo vierund achtzig"), "hallo vier und achtzig")

print("test stringUtil.parseNumber()")
assertEqual(stringUtil.parseNumber("einundzwanzig"), 21)
assertEqual(stringUtil.parseNumber("einsundzwanzig"), 21)
assertEqual(stringUtil.parseNumber("hundertzwei"), 102)
assertEqual(stringUtil.parseNumber("einhundertdreiunddreißig"), 133)
assertEqual(stringUtil.parseNumber("zweitausend vierhundert vierundvierzig"), 2444)
assertEqual(stringUtil.parseNumber("hallo vierund achtzig"), 84)

print("test stringUtil.word2Num()")
assertEqual(stringUtil.word2Num("eins und zwanzig"), 21)
assertEqual(stringUtil.word2Num("hundert zwei"), 102)
assertEqual(stringUtil.word2Num("ein hundert drei und dreizig"), 133)
assertEqual(stringUtil.word2Num("zwei tausend vier hundert vier und vierzig"), 2444)
assertEqual(stringUtil.word2Num("hallo vier und achtzig"), 84)

print("test stringUtil.anyExists()")
assertEqual(stringUtil.anyExists("eins zwei drei", ["vier", "drei"]), True)
assertEqual(stringUtil.anyExists("eins zwei drei", ["fünf", "sieben"]), False)
assertEqual(stringUtil.anyExists("hundert drei", ["alles", "und"]), True)
assertEqual(stringUtil.anyExists("hundert drei", ["alles", "und"], padWhitespace=True), False)
assertEqual(stringUtil.anyExists("hundert drei", ["drei", "test"], padWhitespace=True), True)
