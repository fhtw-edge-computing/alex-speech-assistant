from word2numberi18n import w2n
w2nInstance = w2n.W2N(lang_param='de')

numberWords = [
		"dreizehn",
		"vierzehn",
		"fünfzehn",
		"sechzehn",
		"siebzehn",
		"achtzehn",
		"neunzehn",
		"zwanzig",
		"dreißig",
		"dreizig",
		"vierzig",
		"fünfzig",
		"sechzig",
		"siebzig",
		"achtzig",
		"neunzig",
		"hundert",
		"tausend",
		"ein",
		"eins",
		"zwei",
		"drei",
		"vier",
		"fünf",
		"sechs",
		"sieben",
		"acht",
		"neun",
		"zehn",
		"elf",
		"zwölf",
		"und"]
		
replaceMap = {
	"dreißig": "dreizig",
		"ein": "eins"
}

def anyEqual(string, array):
    for elem in array:
        if elem == string:
            return True
            
    return False
    
def anyExists(string, array):
    return whichExistsIn(string, array) != -1
        
def whichExistsIn(string, array):
    for index, elem in enumerate(array):
        if elem in string:
            return index
            
    return -1

def prepareWordForNumConversion(word):
    i = whichExistsIn(word, numberWords)
    if i != -1:
        replacement = replaceMap.get(numberWords[i]) if replaceMap.get(numberWords[i]) else numberWords[i]
        word = word.replace(numberWords[i], f' {replacement} ')
        return prepareStringForNumConversion(word)
    return word

def prepareStringForNumConversion(string):
    array = string.split();
    for index, item in enumerate(array):
        if anyExists(item, numberWords) and not anyEqual(item, numberWords):
            array[index] = prepareWordForNumConversion(item)
    
    return " ".join(array)
           
def parseNumber(text):
    numText = prepareStringForNumConversion(text)
    numText = " ".join(numText.split());
    try:
        return w2nInstance.word_to_num(numText)
    except:
        return None
    
    return None
    
def word2Num(word):
	try:
		return w2nInstance.word_to_num(word)
	except:
		return None
