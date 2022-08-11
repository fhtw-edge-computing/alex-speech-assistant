import re
import math
from word2numberi18n import w2n
from Levenshtein import distance as levdist
from difflib import SequenceMatcher
import importlib

util = importlib.import_module("util")

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
    
negativeNumberWord = "minus"
piWord = ".*kreis.*zahl.*"
eulerWord = ".*eule.*zahl.*"
    
replaceMap = {
    "dreißig": "dreizig",
    "ein": "eins",
    "sex": "sechs"
}

def anyEqual(string, array):
    for elem in array:
        if elem == string:
            return True
            
    return False

# returns if any elem of array exists in string   
def anyExists(string, array, padWhitespace=False):
    return whichExistsIn(string, array, padWhitespace) != -1
    
def anyWordExists(string, array):
    return anyExists(string, array, padWhitespace=True)

def whichExistsIn(string, array, padWhitespace=False):
    for index, elem in enumerate(array):
        elem = elem if not padWhitespace else f' {elem} '
        string = string if not padWhitespace else f' {string} '
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

def parseNumber(text, lang="de"):
    numText = prepareStringForNumConversion(text)
    numText = " ".join(numText.split());
    num = None
    w2nInstance = w2n.W2N(lang_param=lang)
    try:
        num = w2nInstance.word_to_num(numText)
    except:
        pass
        
    if util.isNumber(num) and negativeNumberWord in text:
            num = num * (-1)
    if (not util.isNumber(num)) and re.match(piWord, text):
        num = math.pi
    if (not util.isNumber(num)) and re.match(eulerWord, text):
        num = math.e
    
    return num

def isRegexPhrase(phrase):
    return '*' in phrase or '{' in phrase

def phraseToRegex(phrase):
    phrase = re.sub('\s+', '', phrase)
    phrase = phrase.replace('*', '.*')
    return f'.*{phrase}.*'

def getLevDistance(str1, str2):
    return levdist(str1, str2)
    
def gitDifflibDistance(str1, str2):
    s = SequenceMatcher(lambda x: x == " ",
                    str1,
                    str2)
    return s.ratio();

#regex = phraseToRegex("* küchenlicht * {num} prozent")
#print(re.match(regex, "üchenlicht 30 prozent"))
