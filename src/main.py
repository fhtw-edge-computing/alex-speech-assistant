#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import re
import importlib

stringUtil = importlib.import_module("stringUtil")
actionHandler = importlib.import_module("actionHandler")


configFile = "config.json"
config = None
q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-c', '--config', type=str, metavar='FILENAME',
    help='config file to read configuration')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

def handlePartial(text):
    if len(text) > 0:
        print("stopping!!!")
        actionHandler.stop()
    
    for stopWord in config["stopWords"]:
        print(stopWord)
        print(text)
        if stopWord in text:
            print("stopping!!!")
            actionHandler.stop()
        

def handleResult(text):
    matchingItems = []
    for item in config["items"]:
        item = setItemDefaults(item)
        if item:
            rec = item["recognition"]
            for phrase in rec["phrases"]:
                if not stringUtil.isRegexPhrase(phrase) and phrase in text:
                    matchingItems.append(item)
                elif stringUtil.isRegexPhrase(phrase):
                    regex = stringUtil.phraseToRegex(phrase)
                    if re.match(regex, text):
                        matchingItems.append(item)
    
    print("matching items:")
    print(matchingItems)
    if len(matchingItems) > 0:
        actionHandler.doAction(matchingItems[0], text)
        q.queue.clear()
    
                
        
def setItemDefaults(item):
    if not item or not item["actionType"] or not item["recognition"]:
        return None
        
    item["recognition"]["phrases"] = item["recognition"].get("phrases") or []
    return item
        

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(lang="de")
    
    configFile = args.config or configFile
    with open(configFile, "r") as f:
        config = json.load(f);
        
    print(config);
            

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            #rec = vosk.KaldiRecognizer(model, args.samplerate)
            rec = vosk.KaldiRecognizer(model, args.samplerate)
            #rec = vosk.KaldiRecognizer(model, args.samplerate, '["oh one two three four five six seven eight nine zero", "[unk]"]')
            #spk_model_path = "/home/pi/vosk-models/vosk-model-spk-0.4"
            #spk_model = vosk.SpkModel(spk_model_path)
            #rec.SetSpkModel(spk_model)
            # rec.SetMaxAlternatives(10) Alternative results ausgeben
            #rec.SetWords(True) #einzelne Wörter mit Zeiten ausgeben
            # rec.SetPartialWords(True) dasselbe bei partials
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    handleResult(result["text"]);
                    print(result)
                    print("---")
                else:
                    partial = json.loads(rec.PartialResult())
                    handlePartial(partial["partial"]);
                    print(partial)
                    print("---")

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
