from pymusician import constants, utils
from numpy import log2
import re

class _Mode:

    def __init__(self,root,mode):
        from pymusician import Note
        if root.__class__.__name__ == "Note":
            self._root = root
        else:
            try:
                self._root = Note(root.capitalize())
            except:
                raise ValueError("Mode root should be a Note object or a valid note name (str).")
        if mode not in constants.MODES:
            raise KeyError("Mode not found.  View the modes json to see/add modes.")
        self._mode = mode
        self._name = self.root.name + " " + mode
        self._spelling = utils.mode_speller(self.root,self.mode)

class _Chord:

    def __init__(self,symbol):
        from pymusician import Note, Interval

        self._symbol = symbol

        data = utils.parse_symbol(symbol)
        self._root = Note(data["root"])
        self._quality = data["quality"]
        self._intervals = data["intervals"]

        spelling = [self.root]
        intvls = []
        for intvl in self._intervals.split():
            if intvl not in intvls:
                spelling.append(self.root + Interval(intvl))
                intvls.append(intvl)

        self._spelling = tuple(spelling)

class _TimeSignature:

    def __init__(self,top_number,bottom_number):
        if not (isinstance(top_number,(int,float)) and
                isinstance(bottom_number,int)):
            raise ValueError("Time signature must be intialized via two numbers (top, bottom).")
        if bottom_number not in constants.TIME_DIVISIONS:
            raise ValueError("Bottom time signature number must be a common power of 2: (1,2,4,8,16,32,64,128,256,512)")
        if top_number < 1:
            raise ValueError("Top time signature number must be 1 or greater.")

        self._top = top_number
        self._bottom = bottom_number

        self._beat_len = constants.RHYTHM_VALUES[int(log2(bottom_number)) + 1]

        self._gets_beat = constants.RHYTHM_NAMES[self._beat_len]

        self._measure_len = self._beat_len * self._top