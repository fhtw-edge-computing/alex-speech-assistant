# Alex offline speech assistant
The aim of this project was to create an offline speech assistant solely based on FOSS software. It uses [vosk-api](https://github.com/alphacep/vosk-api) for speech recognition and a rules in order to map the recognized speech to actions.

While working on this project I discovered [Rhasspy](https://rhasspy.readthedocs.io/en/latest/) and moved on to working on [Rhasspy Bridge](https://github.com/fhtw-edge-computing/rhasspy-bridge) insted of following the approach of this project. Therefore it possibly won't be continued.

## Getting started
* install `vosk-api` according to their [vosk installation steps](https://alphacephei.com/vosk/install)
* download and install speech models for `vosk` according to their [docs on models](https://alphacephei.com/vosk/models)
* install `Pico TTS` using `sudo apt-get install libttspico-utils`
* clone this repository
* `cd src`
* `python3 main.py`

## Features
Features can be seen in the file [config.json](https://github.com/fhtw-edge-computing/alex-speech-assistant/blob/main/src/config.json). All is in German and could also be translated to English or another language and combined with another speech model from `vosk`.

Basically the current features are:
* getting the current date/time
* telling the weather in Vienna
* telling a random joke
* control some smart home items using openHAB
* do calculations:
   * possible calculations are: add, substract, divide, multiply, log, square, squareroot
   * it's possible to use the result of the last calculation by the word `Ergebnis`
   * examples: `rechne 10 mal 10`, and `rechne logarithmus ergebnis` afterwards
   
All of the features are also possible using `Rhasspy` and `Rhasspy Bridge` except doing calculations.

## Differences to Rhasspy combined with Rhasspy Bridge
* Rhasspy is very flexible and can be freely configured using different systems for instance for TTS and STT
* Using regular expressions and real STT this project is more flexible in terms of being able to say things in different ways. E.g. it's possible to say `Schalte das Licht in der Küche ein` and `Licht in der Küche ein` and `Bitte mach das Licht in der Küche aus` and all should work (if the transcription of the speech is correctly recognized). Trying to do the same thing in Rhasspy drastically reduced recognition performance, see [Rhasspy: avoid too complex config](https://github.com/fhtw-edge-computing/rhasspy-bridge#rhasspy-avoid-too-complex-config).
* If reduced to a simple and limited command set I think recognition of Rhasspy is better since it tries to map everything to the known commands. On the other hand the attempt of this project completely fails if the STT engine understands e.g. `Kirche` instead of `Küche`.
