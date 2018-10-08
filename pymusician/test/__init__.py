from pymusician import _pymusician
from pymusician import constants
from pymusician import utils
import re

VERSION = "1.0-0-beta"

A4 = 440

class Note(_pymusician._Note):

    def __init__(self,*args):
        super().__init__(*args)

    @property
    def name(self):
        return self._name
    
    @property
    def letter(self):
        return constants.NOTE_VALUES[self.name[0]][0]
    
    @property
    def pitch(self):
        return utils.pitch_from_name(self.name)
    
    @property
    def octave(self):
        return self._octave
    
    @octave.setter
    def octave(self,value):
        if not isinstance(value,int):
            raise ValueError("Octave value must be None or int.")
        self._octave = value

    @property
    def rhythm(self):
        return utils.rhythm_obj(self._rhythm)

    @rhythm.setter
    def rhythm(self,flags):
        self._rhythm = flags
    
    @property
    def pitch_offset(self):
        pitch_offset = len(self.name) - 1
        if "b" in self.name:
            pitch_offset *= -1
        return pitch_offset
    
    @property
    def hard_pitch(self):
        if self.octave == None:
            return None
        return self.pitch + self.octave * 12
    
    @property
    def frequency(self):
        if self.octave == None:
            return None
        offset = self.hard_pitch - 57
        return A4 * 2**(offset / 12)

    def enharmonic(self,prefer=None,gross=False):
        return utils.enharmonic(self,prefer,gross)
    
    @staticmethod
    def from_values(letter,pitch):
        return Note(utils.note_name_from_values(letter,pitch))
    
    @staticmethod
    def from_hard_pitch(hard_pitch,prefer=None):
        return Note(*utils.note_names_from_hard_pitch(hard_pitch,prefer))

    @staticmethod
    def from_frequency(Hz,prefer=None):
        return Note(*utils.note_names_from_frequency(Hz,prefer))

    def __repr__(self):
        rep = f'<Note {self.name}{str(self.octave if self.octave != None else "")}'\
        f'{":" + self._rhythm if self._rhythm else ""}>'
        return rep

    def __add__(self,intvl_obj):
        return utils.note_plus_intvl(self,intvl_obj)

    def __sub__(self,intvl_obj):
        return utils.note_minus_intvl(self,intvl_obj)

class Interval(_pymusician._Interval):

    def __init__(self,*args):
        super().__init__(*args)
    
    @property
    def diff(self):
        return utils.intvl_diff(self._flags,self._displace)
    
    @property
    def letter_diff(self):
        return int(self._flags[-1]) - 1

    @property
    def name(self):
        return utils.intvl_namer(self)
    
    @staticmethod
    def from_notes(note_obj1,note_obj2):
        if type(note_obj1) is not Note or type(note_obj2) is not Note:
            raise ValueError("Invalid Note object passed.")
        return utils.intvl_from_notes(note_obj1,note_obj2)

    def __repr__(self):
        return f'<Interval {self.name}>'

class Mode:

    def __init__(self,root,mode):

        if type(root) is Note:
            self._root = root
        else:
            try:
                self._root = Note(root.capitalize())
            except:
                raise ValueError("Mode root should be a Note object or note name (str).")
        if mode not in constants.MODES:
            raise KeyError("Mode not found.  View the modes json to see/add modes.")
        self._mode = mode

    @property
    def root(self):
        return self._root

    @property
    def mode(self):
        return self._mode

    @property
    def name(self):
        return self.root.name + " " + self.mode
    
    @property
    def spelling(self):
        return utils.mode_speller(self.root,self.mode)

    def __iter__(self):
        return iter(self.spelling)
    
    def __len__(self):
        return len(self.spelling)
    
    def __getitem__(self,key):
        return self.spelling[key]

    def __repr__(self):
        return f"<Mode {self.name}>"

class Chord:

    def __init__(self,symbol):
        self._symbol = symbol
        self._data = utils.parse_symbol(symbol)
    
    @property
    def symbol(self):
        return self._symbol

    @property
    def root(self):
        return Note(self._data["root"])

    @property
    def quality(self):
        return self._data["quality"]

    @property
    def intervals(self):
        return self._data["intervals"]

    @property
    def spelling(self):
        spelling = [self.root]
        intvls = []
        for intvl in self.intervals.split():
            if intvl not in intvls:
                spelling.append(self.root + Interval(intvl))
                intvls.append(intvl)
        return spelling

    def __iter__(self):
        return iter(self.spelling)
    
    def __len__(self):
        return len(self.spelling)

    def __getitem__(self,key):
        return self.spelling[key]

    def __repr__(self):
        return f"<Chord {self.symbol}>"