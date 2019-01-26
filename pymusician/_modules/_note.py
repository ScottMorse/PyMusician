import re

NOTE_REGEX = r'^[A-Ga-g]([#]*$|[b]*$)'
RHYTHM_REGEX = r'^(10|[0-9])[\.]*[t]?$'

class _Note:

    def __init__(self,name,octave=None,rhythm=None,dots=None,triplet=None):
        name = name.strip().capitalize()
        if not re.match(NOTE_REGEX,name):
            raise ValueError("Invalid Note name.")
        self._name = name
        if octave:
            if not isinstance(octave,int):
                raise ValueError("Octave value must be None or int.")
        self._octave = octave
        if rhythm:
            if isinstance(rhythm,int):
                rhythm = str(rhythm)
            if not isinstance(rhythm,str):
                raise ValueError("Rhythm value should be given as a string of flags.")
            if not re.match(RHYTHM_REGEX,rhythm):
                raise ValueError("Invalid rhythm flags.")
        self._rhythm = rhythm