from pymusician import constants
import re

class _Note:

    def __init__(self,name,octave=None,rhythm=None,dots=None,triplet=None):
        name = name.strip().capitalize()
        if not re.match(constants.NOTE_REGEX,name):
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
            if not re.match(constants.RHYTHM_REGEX,rhythm):
                raise ValueError("Invalid rhythm flags.")
        self._rhythm = rhythm

class _Interval:

    def __init__(self,flags,displace=0):
        flags = flags.strip()
        if not isinstance(flags, str):
            raise ValueError("Interval flags (first argument) should be a string.")
        if not re.match(constants.INT_FLAG_REGEX,flags):
            raise ValueError("Invalid interval flags.  (see documentation)")
        if not isinstance(displace,int):
            raise ValueError("Displacement value should be a positive integer or 0(default).")
        if displace < 0:
            raise ValueError("Displacement value should be a positive integer or 0(default).")
        self._flags = flags
        self._displace = displace

class Metronome(threading.Thread):

    def __init__(self,bpm,count,func=None,*func_args,**kwargs):
        super().__init__(**kwargs)
        if not isinstance(bpm,float) and not isinstance(bpm,int):
            raise ValueError("Metronome bpm must be a number.")
        if not isinstance(count,int):
            raise ValueError("Metronome count must be a positive integer.")
        if count <= 0:
            raise ValueError("Metronome count must be a positive integer.")
        if func:
            if not callable(func):
                raise ValueError('func parameter for Metronome must be a callable object.')
        self._bpm = bpm
        self._count = count
        self._func = func
        self._func_args = func_args
    
    def __repr__(self):
        return f"<Metronome {self.bpm} bpm>"