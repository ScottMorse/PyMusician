from pymusician import _pymusician
from pymusician import constants
from pymusician import utils
import re

VERSION = "1.0.2"

A4 = 440

class Note(_pymusician._Note):

    def __init__(self,*args):
        super().__init__(*args)

    #string (A#, Bb, C, etc.)
    @property
    def name(self):
        return self._name
    
    #int in range 0-6
    @property
    def letter(self):
        return constants.NOTE_VALUES[self.name[0]][0]
    
    #int in range 0-11
    @property
    def pitch(self):
        return utils.pitch_from_name(self.name)
    
    #int representing Scientific Pitch Notation-style octave
    @property
    def octave(self):
        return self._octave
    
    #allows octave to be assigned to Note after instantiation
    @octave.setter
    def octave(self,value):
        if not isinstance(value,int):
            raise ValueError("Octave value must be None or int.")
        self._octave = value

    #A Rhythm object created from the flags of the rhythm or None if no rhythm is provided
    @property
    def rhythm(self):
        return utils.rhythm_obj(self._rhythm)

    #Allows the rhythm to be assigned to the Note directly after instantiation
    @rhythm.setter
    def rhythm(self,flags):
        self._rhythm = flags
    
    #int representing how many half steps (positive, negative or 0) a note's pitch is from the natural note
    @property
    def pitch_offset(self):
        pitch_offset = len(self.name) - 1
        if "b" in self.name:
            pitch_offset *= -1
        return pitch_offset
    
    #int representing the pitch of a Note which has an octave value, starting at 0 for C0
    @property
    def hard_pitch(self):
        if self.octave == None:
            return None
        return self.pitch + self.octave * 12
    
    #float representing the frequency value of a Note whcih has an octave value in Hz
    @property
    def frequency(self):
        if self.octave == None:
            return None
        offset = self.hard_pitch - 57
        return A4 * 2**(offset / 12)

    #method which returns a new Note object which is enharmonic to the current one
    #does NOT affect the object in place
    #prefer can be set to '#' or 'b' to force preference of sign
    #gross set to True treats B#, Cb, E#, and Fb as being as fair game as any other commmon note
    def enharmonic(self,prefer=None,gross=False):
        return utils.enharmonic(self,prefer,gross)
    
    #Instantiates a Note object from letter and pitch value
    #Optional octave and rhythm
    #prefer set to '#' or 'b' forces accidental
    @staticmethod
    def from_values(letter,pitch,octave=None,rhythm=None):
        return Note(utils.note_name_from_values(letter,pitch),octave,rhythm)
    
    #Instantiates a Note object from letter and pitch value
    #Optional rhythm
    #prefer set to '#' or 'b' forces accidental
    @staticmethod
    def from_hard_pitch(hard_pitch,prefer=None,rhythm=None):
        return Note(*utils.note_names_from_hard_pitch(hard_pitch,prefer),rhythm)

    #Instantiates a Note object from letter and pitch value
    #Optional rhythm
    #prefer set to '#' or 'b' forces accidental
    @staticmethod
    def from_frequency(Hz,prefer=None,rhythm=None):
        return Note(*utils.note_names_from_frequency(Hz,prefer),rhythm)

    def __repr__(self):
        rep = f'<Note {self.name}{str(self.octave if self.octave != None else "")}'\
        f'{":" + self._rhythm if self._rhythm else ""}>'
        return rep

    #Allows the addition of a Note object plus an Interval object to return a new Note
    def __add__(self,intvl_obj):
        return utils.note_plus_intvl(self,intvl_obj)

    #Allows the subtraction of a Note object minus an Interval object to return a new Note
    def __sub__(self,intvl_obj):
        return utils.note_minus_intvl(self,intvl_obj)

class Interval(_pymusician._Interval):

    def __init__(self,*args):
        super().__init__(*args)
    
    #int representing the distance in pitch of the interval
    @property
    def diff(self):
        return utils.intvl_diff(self._flags,self._displace)
    
    #int representing the distance in letter of the interval
    @property
    def letter_diff(self):
        return int(self._flags[-1]) - 1

    #string representing a musician-friendly interval name
    @property
    def name(self):
        return utils.intvl_namer(self)
    
    #instantiates an interval from the distance between two Note objects (octave or no octave considered)
    @staticmethod
    def from_notes(note_obj1,note_obj2):
        if type(note_obj1) is not Note or type(note_obj2) is not Note:
            raise ValueError("Invalid Note object passed.")
        return utils.intvl_from_notes(note_obj1,note_obj2)

    def __repr__(self):
        return f'<Interval {self.name}>'

class Mode:

    #can be initialized with a string or Note object root
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

    #A Note object
    @property
    def root(self):
        return self._root

    #string, the mode quality name
    @property
    def mode(self):
        return self._mode

    #string, full root + mode name
    @property
    def name(self):
        return self.root.name + " " + self.mode
    
    #A tuple of Note objects
    @property
    def spelling(self):
        return utils.mode_speller(self.root,self.mode)

    #Iterating a Mode iterates over the spelling
    def __iter__(self):
        return iter(self.spelling)
    
    #The length comes from the spelling as well
    def __len__(self):
        return len(self.spelling)
    
    #Can index the Mode's spelling
    def __getitem__(self,key):
        return self.spelling[key]

    def __repr__(self):
        return f"<Mode {self.name}>"

class Chord:

    #Initialized with a string chord symbol
    def __init__(self,symbol):
        self._symbol = symbol
        self._data = utils.parse_symbol(symbol)
    
    #The original symbol
    @property
    def symbol(self):
        return self._symbol

    #A Note object
    @property
    def root(self):
        return Note(self._data["root"])

    #The quality name string
    @property
    def quality(self):
        return self._data["quality"]

    #The string of intervals used
    @property
    def intervals(self):
        return self._data["intervals"]

    #Similar to the Mode class, a tuple of Note objects
    @property
    def spelling(self):
        spelling = [self.root]
        intvls = []
        for intvl in self.intervals.split():
            if intvl not in intvls:
                spelling.append(self.root + Interval(intvl))
                intvls.append(intvl)
        return tuple(spelling)

    #Like Mode class, can iterate, get length, and index the spelling on the object
    def __iter__(self):
        return iter(self.spelling)
    
    def __len__(self):
        return len(self.spelling)

    def __getitem__(self,key):
        return self.spelling[key]

    def __repr__(self):
        return f"<Chord {self.symbol}>"