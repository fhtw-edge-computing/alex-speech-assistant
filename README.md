# alex-speech-assistant

# libffi.so.6 not found
https://github.com/rhasspy/rhasspy/issues/290

# Training failed exception, german numbers not working
https://github.com/rhasspy/rhasspy/issues/294

# Audio recording not working
https://github.com/rhasspy/rhasspy/issues/293

# picovoice other wakewords
https://github.com/Picovoice/porcupine/issues/617

# Rhasspy

## complex config
```
[ChangePanelLightState]
rooms = (schlafzimmer | wohnzimmer | kueche | (seminarraum | seminarbereich):seminarraum | labor){room}
light_state = (ein:100 | aus:0) {value}
\[schalte] [das] deckenlicht [(im | in (der | dem))] <rooms> [auf] (0..100){value} prozent
\[(im | in (der | dem))] <rooms>[das] deckenlicht [auf] (0..100){value} prozent
\[schalte] [das] deckenlicht [(im | in (der | dem))] <rooms> [auf] <light_state>
\[(im | in (der | dem))] <rooms>[das] deckenlicht [auf] <light_state> [schalten]

[ChangeLightState]
alle = (alle lichter | alle leuchten):alle
esstisch = (([licht beim] esstisch) | (esstisch [licht])):esstisch
kochtisch = (([licht beim] (kochtisch | kochfeld)) | ((kochtisch | kochfeld) [licht])):kochtisch
wohnzimmer = (([licht beim] wohnzimmertisch) | (wohnzimmertisch [licht]) | (haengelampe [im] wohnzimmer) | (haengelampe [beim] wohnzimmertisch) | haengelampe):wohnzimmertisch
wand = ((wandlicht [schlafzimmer]) | ([schlafzimmer] wandlicht)):wand
bad = ((licht [im] bad) | badlicht):bad
gang = ((licht am gang) | ganglicht):gang
light_state = (ein:ON | aus:OFF) {value}
light_name = (alle | esstisch | kochtisch | wohnzimmer | wand | bad | gang){name}
\[schalte] [das | die] <light_name> <light_state>
\[das] [licht] [(am | im | in (der | dem))] <light_name> <light_state>[schalten]
```
