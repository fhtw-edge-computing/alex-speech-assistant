from subprocess import Popen, run

speakHandler = None

def speak(text):
	global speakHandler
	stopSpeaking()
	print(f'speaking text: {text}')
	run(['pico2wave', '--lang=de-DE', '-w', '/tmp/pico.wav', f'"{text}"'])
	speakHandler = Popen(['aplay', '/tmp/pico.wav'])


def stopSpeaking():
	global speakHandler
	if speakHandler:
		speakHandler.terminate()
	run(['rm', '-f', '/tmp/pico.wav'])
	speakHandler = None
	
