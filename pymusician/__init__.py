from pymusician._modules import _note, _interval, _mode, _chord, _timesignature

VERSION = "1.1.1"

class A4:

    __A4 = 440

    @staticmethod
    def getA4():
        return A4.__A4

    @staticmethod
    def setA4(Hz):
        if not isinstance(Hz,(int,float)):
            raise ValueError("A4 must be set to a number.")
        if Hz <= 0:
            raise ValueError("A4 must be a number greater than 0.")
        A4.__A4 = Hz

class Note(_note._Note):

    def __init__(self,name,octave=None,rhythm=None,dots=None,triplet=None):
        super().__init__(name,octave,rhythm,dots,triplet)

    #string (A#, Bb, C, etc.)
    @property
    def name(self):
        return self._name
    
    #int in range 0-6
    @property
    def letter(self):
        return self._letter
    
    #int in range 0-11
    @property
    def pitch(self):
        return self._pitch
    
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
        return self._rhythm

    #Allows the rhythm to be assigned to the Note directly after instantiation
    @rhythm.setter
    def rhythm(self,flags):
        if not flags:
            self._rhythm = None
        self._rhythm = _note.Rhythm(flags)
    
    #int representing how many half steps (positive, negative or 0) a note's pitch is from the natural note
    @property
    def pitch_offset(self):
        return self._pitch_offset
    
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
        return A4.getA4() * 2**(offset / 12)

    #method which returns a new Note object which is enharmonic to the current one
    #prefer can be set to '#' or 'b' to force preference of sign
    #gross set to True treats B#, Cb, E#, and Fb as being as fair game as any other commmon note
    def enharmonic(self,prefer=None,gross=False):
        return _note.enharmonic(self,prefer,gross)
    
    #Instantiates a Note object from letter and pitch value
    #Optional octave and rhythm
    #prefer set to '#' or 'b' forces accidental
    @staticmethod
    def from_values(letter,pitch,octave=None,rhythm=None):
        return Note(_note.note_name_from_values(letter,pitch),octave,rhythm)
    
    #Instantiates a Note object from letter and pitch value
    #Optional rhythm
    #prefer set to '#' or 'b' forces accidental
    @staticmethod
    def from_hard_pitch(hard_pitch,prefer=None,rhythm=None):
        return Note(*_note.note_names_from_hard_pitch(hard_pitch,prefer),rhythm)

    #Instantiates a Note object from letter and pitch value
    #Optional rhythm
    #prefer set to '#' or 'b' forces accidental
    @staticmethod
    def from_frequency(Hz,prefer=None,rhythm=None):
        return Note(*_note.note_names_from_frequency(Hz,prefer),rhythm)

    def __repr__(self):
        rep = f'<Note {self.name}{str(self.octave if self.octave != None else "")}'
        if self.rhythm:
            rep += f'{":" + self.rhythm.flags}'
        return rep + '>'

    #Allows the addition of a Note object plus an Interval object to return a new Note
    def __add__(self,intvl_obj):
        return _note.note_plus_intvl(self,intvl_obj)

    #Allows the subtraction of a Note object minus an Interval object to return a new Note
    def __sub__(self,intvl_obj):
        return _note.note_minus_intvl(self,intvl_obj)

class Interval(_interval._Interval):

    def __init__(self,flags,displace=0):
        super().__init__(flags,displace)
    
    #int representing the distance in pitch of the interval
    @property
    def diff(self):
        return self._diff
    
    #int representing the distance in letter of the interval
    @property
    def letter_diff(self):
        return self._letter_diff

    #string representing a musician-friendly interval name
    @property
    def name(self):
        return self._name
    
    #instantiates an interval from the distance between two Note objects (octave or no octave considered)
    @staticmethod
    def from_notes(note_obj1,note_obj2):
        return _interval.intvl_from_notes(note_obj1,note_obj2)

    def __repr__(self):
        return f'<Interval {self.name}>'

class Mode(_mode._Mode):

    #can be initialized with a string or Note object root
    def __init__(self,root,mode):
        super().__init__(root,mode)

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
        return self._name
    
    #A tuple of Note objects
    @property
    def spelling(self):
        return self._spelling

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

class Chord(_chord._Chord):

    #Initialized with a string chord symbol
    def __init__(self,symbol):
        super().__init__(symbol)
    
    #The original symbol
    @property
    def symbol(self):
        return self._symbol

    #A Note object
    @property
    def root(self):
        return self._root

    #The quality name string
    @property
    def quality(self):
        return self._quality

    #The string of intervals used
    @property
    def intervals(self):
        return self._intervals

    #Similar to the Mode class, a tuple of Note objects
    @property
    def spelling(self):
        return self._spelling

    #!TODO
    # @staticmethod
    # def from_notes(*notes, root=None):
    #     return _chord.chord_from_notes(*notes,root=root)

    #Like Mode class, can iterate, get length, and index the spelling on the object
    def __iter__(self):
        return iter(self.spelling)
    
    def __len__(self):
        return len(self.spelling)

    def __getitem__(self,key):
        return self.spelling[key]

    def __repr__(self):
        return f"<Chord {self.symbol}>"

class TimeSignature(_timesignature._TimeSignature):

    #intialized with the two numbers as seen on sheet music: (4,4) for common time, (3,4) for waltz
    def __init__(self,top_number,bottom_number):
        super().__init__(top_number,bottom_number)

    #numeric
    @property
    def top_number(self):
        return self._top
    
    #numeric
    @property
    def bottom_number(self):
        return self._bottom

    #returns string name of the rhythm that gets the beat
    @property
    def gets_beat(self):
        return self._gets_beat

    #the length of a single beat in 512th notes (numeric)
    @property
    def beat_len(self):
        return self._beat_len

    #the total length of a measure in 512th notes (numeric)
    @property
    def measure_len(self):
        return self._measure_len