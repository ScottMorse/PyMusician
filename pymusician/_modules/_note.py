import re
from numpy import log2

NOTE_REGEX = r'^[A-Ga-g]([#]*$|[b]*$)'
NOTE_VALUES = {
    "C": (0,0), "D": (1,2),
    "E": (2,4), "F": (3,5),
    "G": (4,7), "A": (5,9),
    "B": (6,11),
}
RHYTHM_REGEX = r'^(10|[0-9])[\.]*[t]?$'
RHYTHM_VALUES = [
    1024,512,256,128,
    64,32,16,8,4,2,1,
]

GROSS_ROOTS = {"B":"Cb","C":"B#","E":"Fb","F":"E#"}
NON_NATURAL = (1,3,6,8,10)

class _Note:

    def __init__(self,name,octave=None,rhythm=None,dots=None,triplet=None):
        name = name.strip().capitalize()
        if not re.match(NOTE_REGEX,name):
            raise ValueError("Invalid Note name.")

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
            self._rhythm = Rhythm(rhythm)
        else:
            self._rhythm = None

        pitch_offset = len(name) - 1
        if "b" in name:
            pitch_offset *= -1

        self._name = name
        self._letter = NOTE_VALUES[name[0]][0]
        self._pitch = pitch_from_name(name)
        self._pitch_offset = pitch_offset

class Rhythm:

    def __init__(self,flags):
        if flags == None:
            return
        if isinstance(flags,int):
            flags = str(flags)
        if not isinstance(flags,str):
            raise ValueError("Invalid rhythm flags.")
        flags = flags.replace(" ","")
        if not re.match(RHYTHM_REGEX,flags):
            raise ValueError("Invalid rhythm flags.")
        dots = 0
        triplet = False
        if len(flags) > 1:
            if flags[1] == "0":
                num = 10
                value = 1024
            else:
                num = int(flags[0])
            for char in flags:
                if char == ".":
                    dots += 1
                if char == "t":
                    triplet = True
            value = RHYTHM_VALUES[num]

            if dots:
                original_value = value
                for i in range(dots):
                    value += original_value/(2**(i + 1))
            
            if triplet:
                value *= (2/3)

        else:
            num = int(flags[0])
            value = RHYTHM_VALUES[num]

        self.value = value
        self.dots = dots
        self.triplet = triplet
        self.num = num
        self.flags = flags

    def __repr__(self):
        return f"<Rhythm object {self.flags} val:{round(self.value,2)}>"

#assigns pitch integer value to a Note based on it's name
def pitch_from_name(name):
    pitch = NOTE_VALUES[name[0]][1]
    if len(name) > 1:
        if name[1] == "#":
            pitch += len(name) - 1
            if pitch > 11:
                pitch -= 12
        else:
            pitch -= len(name) - 1
            if pitch < 0:
                pitch += 12
    return pitch

#returns new Note object enharmonic to the old
def enharmonic(note_obj,prefer=None,gross=False):
    from pymusician import Note

    if prefer:
        if prefer not in ("#","b"):
            raise ValueError("'prefer' parameter should be set to '#' or 'b'.")
    if not isinstance(gross, bool):
        raise ValueError("2nd arg for enharmonic should be Boolean.")

    if gross and note_obj.name in GROSS_ROOTS:
        new_name = GROSS_ROOTS[note_obj.name]
        if "#" in new_name and prefer == 'b':
            return note_obj
        elif 'b' in new_name and prefer == '#':
            return note_obj
        else:
            new_note = Note(new_name)
    elif len(note_obj.name) == 1:
        return note_obj
    elif len(note_obj.name) == 2:
        if "#" in note_obj.name:
            if prefer == '#':
                return note_obj
            new_letter = note_obj.letter + 1
            if new_letter > 6:
                new_letter -= 7
        else:
            if prefer == 'b':
                return note_obj
            new_letter = note_obj.letter - 1
            if new_letter < 0:
                new_letter += 7
        new_note = Note.from_values(new_letter,note_obj.pitch)
    else:
        new_note = note_obj
        new_letter = note_obj.letter
        limit = 2 if note_obj.pitch in NON_NATURAL else 1
        while len(new_note.name) > limit:
            if "#" in note_obj.name:
                new_letter += 1
                if new_letter > 6:
                    new_letter -= 7
            else:
                new_letter -= 1
                if new_letter < 0:
                    new_letter += 7
            new_note = Note.from_values(new_letter,note_obj.pitch)
        if "#" in new_note.name and prefer == "b":
            new_note = Note.from_values(new_letter + 1, note_obj.pitch)
        elif "b" in new_note.name and prefer == "#":
            new_note = Note.from_values(new_letter - 1, note_obj.pitch)
    if note_obj.octave:
        new_note.octave = note_obj.octave
    if note_obj.rhythm:
        new_note.rhythm = note_obj.rhythm.flags
    return new_note

#Used as in a static method by the note class to instantiate a Note from a letter and pitch value
#This returns only the string name of the note
def note_name_from_values(letter,pitch):
    if letter not in range(7):
        raise ValueError("Letter argument should be an integer between 0 and 6, 0 for C, 1 for B, etc.")
    if pitch not in range(12):
        raise ValueError("Pitch argument should be an integer between 0 and 11, 0 for C natural (or equivalent), 1 for C#/Db, etc.")
    letter_str = tuple(NOTE_VALUES.keys())[letter]
    expected_pitch = NOTE_VALUES[letter_str][1]
    pitch_offset = pitch - expected_pitch
    if pitch_offset > 5:
        pitch_offset -= 12
    elif pitch_offset < -6:
        pitch_offset += 12
    if pitch_offset == 0:
        return letter_str
    elif pitch_offset < 0:
        return letter_str + "b" * (-1 * pitch_offset)
    return letter_str + "#" * pitch_offset

#Used as a static mehtod by the note class to instantiate a Note from a hard pitch value
#This returns only the string name of the note
def note_names_from_hard_pitch(hard_pitch,prefer=None):
    if type(hard_pitch) is not int:
            raise ValueError("Hard pitch argument must be an integer.")
    if prefer not in ("#","b",None):
        raise ValueError("'prefer' parameter should be set to '#' or 'b'.")
    octave = hard_pitch // 12
    pitch = hard_pitch % 12
    index = 0
    for note_key in NOTE_VALUES:
        if pitch == NOTE_VALUES[note_key][1]:
            return (note_key,octave)
        if pitch == NOTE_VALUES[note_key][1] + 1:
            if prefer == "b":
                if index == 6:
                    index = -1
                return (tuple(NOTE_VALUES.keys())[index + 1] + "b",octave)
            return (note_key + "#",octave)
        index += 1

#Used as a static mehtod by the note class to instantiate a Note from a Hertz value
#This returns only the string name of the note
def note_names_from_frequency(Hz,prefer=None):
    from pymusician import A4

    if type(Hz) is not int and type(Hz) is not float:
            raise ValueError("Please provide a positive number for the Hz value.")
    if Hz <= 0:
        raise ValueError("Please provide a positive number for the Hz value.")
    if prefer not in ("#","b",None):
        raise ValueError("'prefer' parameter should be set to '#' or 'b'.")
    return note_names_from_hard_pitch(int(round(12 * (log2(Hz) - log2(A4.getA4()))) + 57),prefer)

#Returns a note object that is a supplied interval up from the supplied note
#Does not need an octave, but will supply the accurate octave-level of the new note if provided
def note_plus_intvl(note_obj,intvl_obj):
    from pymusician import Note,Interval

    if not isinstance(intvl_obj,Interval):
        raise ValueError("Intervals can only be added to Note objects.")

    letter = note_obj.letter + intvl_obj.letter_diff

    if letter > 6:
        letter -= 7
    if note_obj.octave != None:
        hard_pitch = note_obj.hard_pitch + intvl_obj.diff
        new_note = Note.from_values(letter,hard_pitch % 12)
        new_note.octave = hard_pitch // 12
    else:
        pitch = note_obj.pitch + intvl_obj.diff
        if intvl_obj._displace > 0:
            pitch -= intvl_obj._displace * 12
        if pitch > 11:
            pitch -= 12
        new_note = Note.from_values(letter,pitch)

    if note_obj.rhythm:
        print(note_obj.rhythm)
        new_note.rhythm = note_obj.rhythm.flags

    return new_note

#Returns a note object that is a supplied interval down from the supplied note
#Does not need an octave, but will supply the accurate octave-level of the new note if provided
def note_minus_intvl(note_obj,intvl_obj):
    from pymusician import Note, Interval

    if not isinstance(intvl_obj,Interval):
            raise ValueError("Intervals can only be added to Note objects.")

    letter = note_obj.letter - intvl_obj.letter_diff

    if letter < 0:
        letter += 7
    if note_obj.octave != 0:
        hard_pitch = note_obj.hard_pitch - intvl_obj.diff
        new_note = Note.from_values(letter,abs(hard_pitch % 12))
        new_note.octave = hard_pitch // 12
    else:
        pitch = note_obj.pitch - intvl_obj.diff
        if intvl_obj._displace > 0:
            pitch -= intvl_obj._displace * 12
        if pitch < 0:
            pitch += 12
        new_note = Note.from_values(letter,pitch)

    if note_obj.rhythm:
        print(note_obj.rhythm)
        new_note.rhythm = note_obj.rhythm.flags

    return new_note