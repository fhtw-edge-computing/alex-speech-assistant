import subprocess

speakHandler = None

def speak(text):
	global speakHandler
	stopSpeaking()
	print(f'speaking text: {text}')
	subprocess.run(['pico2wave', '--lang=de-DE', '-w', '/tmp/pico.wav', f'"{text}"'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	speakHandler = subprocess.Popen(['aplay', '/tmp/pico.wav'])


def stopSpeaking():
	global speakHandler
	if speakHandler:
		speakHandler.terminate()
	subprocess.run(['rm', '-f', '/tmp/pico.wav'])
	speakHandler = None
	
