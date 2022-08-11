import subprocess

speakHandler = None
currentLang = "de"

langMapping = {
	"de": "de-DE",
	"en": "en-US"
}

def speak(text):
	global speakHandler
	stopSpeaking()
	print(f'speaking text: {text}')
	subprocess.run(['pico2wave', f'--lang={langMapping.get(currentLang)}', '-w', '/tmp/pico.wav', f'"{text}"'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	speakHandler = subprocess.Popen(['aplay', '/tmp/pico.wav'])


def stopSpeaking():
	global speakHandler
	if speakHandler:
		speakHandler.terminate()
	subprocess.run(['rm', '-f', '/tmp/pico.wav'])
	speakHandler = None
	
def setLang(lang):
	global currentLang
	currentLang = lang
	
