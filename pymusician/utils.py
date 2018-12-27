from pymusician import constants
from numpy import log2
import re
import pymusician

#TODO refactoring speller functions and possibly rethink how rhythm and interval flags are written/parsed.

###NOTE CLASS FUNCTIONS

#assigns pitch integer value to a Note based on it's name
def pitch_from_name(name):
    pitch = constants.NOTE_VALUES[name[0]][1]
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

#Rhythm objects are used as a property of a Note object which has a rhythm value
class Rhythm:

    def __init__(self, value,dots,triplet,num,flags):
        self.value = value
        self.dots = dots
        self.triplet = triplet
        self.num = num
        self.flags = flags

    def __repr__(self):
        return f"<Rhythm object {self.flags} val:{round(self.value,2)}>"

def rhythm_obj(flags):
    #flags should be a string, but this can be forgiven if only a valid integer is passed
    if flags == None:
        return None
    if isinstance(flags,int):
        flags = str(flags)
    if not isinstance(flags,str):
        raise ValueError("Invalid rhythm flags.")
    flags = flags.replace(" ","")
    if not re.match(constants.RHYTHM_REGEX,flags):
        raise ValueError("Invalid rhythm flags.")
    dots = 0
    triplet = False
    if len(flags) > 1:
        if flags[1] == "0":
            num = 10
            val = 1024
        else:
            num = int(flags[0])
        for char in flags:
            if char == ".":
                dots += 1
            if char == "t":
                triplet = True
        val = constants.RHYTHM_VALUES[num]

        if dots:
            original_value = val
            for i in range(dots):
                val += original_value/(2**(i + 1))
        
        if triplet:
            val *= (2/3)

    else:
        num = int(flags[0])
        val = constants.RHYTHM_VALUES[num]

    return Rhythm(val,dots,triplet,num,flags)

#used as a method by the Note class to return a new enharmonic Note object
def enharmonic(note_obj,prefer=None,gross=False):
    if prefer:
        if prefer not in ("#","b"):
            raise ValueError("'prefer' parameter should be set to '#' or 'b'.")
    if not isinstance(gross, bool):
        raise ValueError("2nd arg for enharmonic should be Boolean.")

    if gross and note_obj.name in constants.GROSS_ROOTS:
        new_name = constants.GROSS_ROOTS[note_obj.name]
        if "#" in new_name and prefer == 'b':
            return note_obj
        elif 'b' in new_name and prefer == '#':
            return note_obj
        else:
            new_note = pymusician.Note(new_name)
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
        new_note = pymusician.Note.from_values(new_letter,note_obj.pitch)
    else:
        new_note = note_obj
        new_letter = note_obj.letter
        limit = 2 if note_obj.pitch in constants.NON_NATURAL else 1
        while len(new_note.name) > limit:
            if "#" in note_obj.name:
                new_letter += 1
                if new_letter > 6:
                    new_letter -= 7
            else:
                new_letter -= 1
                if new_letter < 0:
                    new_letter += 7
            new_note = pymusician.Note.from_values(new_letter,note_obj.pitch)
        if "#" in new_note.name and prefer == "b":
            new_note = pymusician.Note.from_values(new_letter + 1, note_obj.pitch)
        elif "b" in new_note.name and prefer == "#":
            new_note = pymusician.Note.from_values(new_letter - 1, note_obj.pitch)
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
    letter_str = constants.NOTES[letter]
    expected_pitch = constants.NOTE_VALUES[letter_str][1]
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
    note_dict = constants.NOTE_VALUES
    for note_key in note_dict:
        if pitch == note_dict[note_key][1]:
            return (note_key,octave)
        if pitch == note_dict[note_key][1] + 1:
            if prefer == "b":
                if index == 6:
                    index = -1
                return (constants.NOTES[index + 1] + "b",octave)
            return (note_key + "#",octave)
        index += 1

#Used as a static mehtod by the note class to instantiate a Note from a Hertz value
#This returns only the string name of the note
def note_names_from_frequency(Hz,prefer=None):
    if type(Hz) is not int and type(Hz) is not float:
            raise ValueError("Please provide a positive number for the Hz value.")
    if Hz <= 0:
        raise ValueError("Please provide a positive number for the Hz value.")
    if prefer not in ("#","b",None):
        raise ValueError("'prefer' parameter should be set to '#' or 'b'.")
    return note_names_from_hard_pitch(int(round(12 * (log2(Hz) - log2(pymusician.A4))) + 57),prefer)

###INTERVAL CLASS FUNCTIONS

#Returns an integer value which describes the distance represented by an Interval
def intvl_diff(flags,_displace):
    intvl_quality = flags[0]
    adder_dots = len(flags) - 2
    intvl_type = flags[-1]
    if intvl_type == '8':
        intvl_type = '1'
        _displace += 1

    base_diff = constants.INTVLS[intvl_type]
    if isinstance(base_diff,tuple):
        if intvl_quality == "M":
            diff = base_diff[1]
        elif intvl_quality == "m":
            diff = base_diff[0]
        elif intvl_quality.lower() == "a":
            diff = base_diff[1] + 1 + adder_dots
        else:
            diff = base_diff[0] - 1 - adder_dots
    else:
        if intvl_quality.lower() == "a":
            diff = base_diff + 1 + adder_dots
        elif intvl_quality.lower() == "d":
            diff = base_diff - 1 - adder_dots
        else:
            diff = base_diff

    if _displace:
        diff += _displace * 12
    
    return diff

#Used to give a musician-friendly full name to an interval from its flags
#Returns a string name
def intvl_namer(intvl):
    if intvl._flags[-1] == "1" and intvl._flags[0].lower() == "p" and intvl._displace > 1 and len(intvl._flags) == 2:
        return f"{intvl._displace} octaves"
    if intvl._displace == 1:
        if intvl._flags[-1] == "1":
            base = "octave"
        else:
            base = str(int(intvl._flags[-1]) + 7) + "th"
    else:
        base = constants.INTVL_NAMES[int(intvl._flags[-1]) - 1]
    if intvl._flags[0] == "M":
        quality = "Major"
    elif intvl._flags[0] == "m":
        quality = "Minor"
    elif intvl._flags[0].lower() == "p":
        quality = "Perfect"
    elif intvl._flags[0].lower() == "a":
        quality = "Augmented"
    else:
        quality = "Diminished"
    if len(intvl._flags) > 2:
        times = f"(x{len(intvl._flags) - 1})"
    else:
        times = ""
    name = quality + times + " " + base
    if intvl._displace > 1:
        name += f" plus {intvl._displace} octaves"
    return name

#Used by a static method by the Interval class to determine an interval from two Note objects
#Directly returns an Interval object
def intvl_from_notes(note_obj1,note_obj2):
    displace = 0
    pitch_diff = note_obj2.pitch - note_obj1.pitch
    letter_diff = note_obj2.letter - note_obj1.letter
    if letter_diff == 0:
        pitch_diff = abs(pitch_diff)
    if pitch_diff < 0:
        pitch_diff += 12
    if letter_diff < 0:
        letter_diff += 7

    if note_obj1.octave != None and note_obj2.octave != None:
        pitch_diff = abs(note_obj1.hard_pitch - note_obj2.hard_pitch)
        displace = pitch_diff // 12
        pitch_diff %= 12
        if note_obj1.hard_pitch > note_obj2.hard_pitch:
            letter_diff = note_obj1.letter - note_obj2.letter
            if letter_diff < 0:
                letter_diff += 7
    
    base_flag = str(letter_diff + 1)
    
    expected_pitch = constants.INTVLS[base_flag]

    if isinstance(expected_pitch, tuple):
        if pitch_diff == expected_pitch[0]:
            flags = "m" + base_flag
        elif pitch_diff == expected_pitch[1]:
            flags = "M" + base_flag
        elif pitch_diff > expected_pitch[1]:
            adder_dots = pitch_diff - (expected_pitch[1] + 1)
            if adder_dots > 5:
                adder_dots = 12 - adder_dots
                quality = "D"
            else:
                quality = "A"
            flags = quality + "." * adder_dots + base_flag
        else:
            adder_dots = pitch_diff - (expected_pitch[1] - 1)
            if adder_dots > 5:
                adder_dots = 12 - adder_dots
                quality = "A"
            else:
                quality = "D"
            flags = quality + "." * adder_dots + base_flag
    else:
        if pitch_diff == expected_pitch:
            flags = "P" + base_flag
        elif pitch_diff > expected_pitch:
            adder_dots = pitch_diff - (expected_pitch + 1)
            if adder_dots > 5:
                adder_dots = 12 - adder_dots
                quality = "D"
            else:
                quality = "A"
            if letter_diff == 0 and note_obj1.pitch_offset > note_obj2.pitch_offset:
                quality = "D"
            flags = quality + "." * adder_dots + base_flag
        else:
            adder_dots = pitch_diff - (expected_pitch - 1)
            if adder_dots > 5:
                adder_dots = 12 - adder_dots
                quality = "A"
            else:
                quality = "D"
            flags = quality + "." * adder_dots + base_flag
    
    intvl = pymusician.Interval(flags,displace)
    return intvl

#Returns a note object that is a supplied interval up from the supplied note
#Does not need an octave, but will supply the accurate octave-level of the new note if provided
def note_plus_intvl(note_obj,intvl_obj):

    letter = note_obj.letter + intvl_obj.letter_diff

    if letter > 6:
        letter -= 7
    if note_obj.octave != None:
        hard_pitch = note_obj.hard_pitch + intvl_obj.diff
        new_note = pymusician.Note.from_values(letter,hard_pitch % 12)
        new_note.octave = hard_pitch // 12
    else:
        pitch = note_obj.pitch + intvl_obj.diff
        if intvl_obj._displace > 0:
            pitch -= intvl_obj._displace * 12
        if pitch > 11:
            pitch -= 12
        new_note = pymusician.Note.from_values(letter,pitch)

    if note_obj.rhythm:
        new_note._rhythm = note_obj.rhythm.flags

    return new_note

#Returns a note object that is a supplied interval down from the supplied note
#Does not need an octave, but will supply the accurate octave-level of the new note if provided
def note_minus_intvl(note_obj,intvl_obj):
    if not isinstance(intvl_obj,pymusician.Interval):
            raise ValueError("Intervals can only be added to Note objects.")

    letter = note_obj.letter - intvl_obj.letter_diff

    if letter < 0:
        letter += 7
    if note_obj.octave != 0:
        hard_pitch = note_obj.hard_pitch - intvl_obj.diff
        new_note = pymusician.Note.from_values(letter,abs(hard_pitch % 12))
        new_note.octave = hard_pitch // 12
    else:
        pitch = note_obj.pitch - intvl_obj.diff
        if intvl_obj._displace > 0:
            pitch -= intvl_obj._displace * 12
        if pitch < 0:
            pitch += 12
        new_note = pymusician.Note.from_values(letter,pitch)

    if note_obj.rhythm:
        new_note._rhythm = note_obj.rhythm.flags

    return new_note

#MODE FUNCTIONS

#returns a tuple of Note objects for the given mode
def mode_speller(root,mode):

    spelling = [root]

    if type(constants.MODES[mode]) is str:
        parent_name = constants.MODES[mode][:len(constants.MODES[mode])-1]
        offset = int(constants.MODES[mode][-1]) - 1
    elif type(constants.MODES[mode]) is list:
        parent_name = mode
        offset = 0
    else:
        raise ValueError("Invalid Mode pattern. (Check modes json)")
    parent = constants.MODES[parent_name]
    for item in parent:
        if type(item) is not int:
            raise ValueError("Invalid Mode pattern. (Check modes json)")
    
    next_pitch = root.pitch
    next_letter = root.letter
    index = offset
    n = 1
    flats = False if "b" not in root.name else True
    sharps = False if "#" not in root.name else True
    if parent_name in constants.MODE_LETTER_SPELLINGS:
        for step in parent:
            if index == len(parent):
                index -= len(parent)
            if n == len(parent):
                break
            next_pitch += parent[index]
            if parent_name in constants.MODE_LETTER_SPELLINGS:
                next_letter += constants.MODE_LETTER_SPELLINGS[parent_name][index]
            else:
                next_letter += 1
            if next_pitch < 0:
                next_pitch += 12
            elif next_pitch > 11:
                next_pitch -= 12
            if next_letter < 0:
                next_letter += 7
            elif next_letter > 6:
                next_letter -= 7
            if parent_name in constants.MODE_LETTER_SPELLINGS:
                next_note = pymusician.Note.from_values(next_letter,next_pitch)
            else:
                next_note = pymusician.Note.from_values(next_letter,next_pitch)
                if len(next_note.name) > 2:
                    next_note = next_note.enharmonic()
                if next_note.name in ("B#","Cb","E#","Fb"):
                    next_note = next_note.enharmonic()
                if "#" in next_note.name:
                    if flats:
                        next_note = next_note.enharmonic()
                    if not flats and not sharps:
                        sharps = True
                if "b" in next_note.name:
                    if sharps:
                        next_note = next_note.enharmonic()
                    if not flats and not sharps:
                        flats = True
            spelling.append(next_note)
            index += 1
            n += 1
    else:
        flats = False if "b" not in root.name else True
        sharps = False if "#" not in root.name else True
        for step in parent:
            if index == len(parent):
                index -= len(parent)
            if n == len(parent):
                break
            next_pitch += parent[index]
            next_letter += 1
            if next_pitch < 0:
                next_pitch += 12
            elif next_pitch > 11:
                next_pitch -= 12
            if next_letter < 0:
                next_letter += 7
            elif next_letter > 6:
                next_letter -= 7
            next_note = pymusician.Note.from_values(next_letter,next_pitch)
            if len(next_note.name) > 2:
                next_note = next_note.enharmonic()
            if next_note.name in ("B#","Cb","E#","Fb"):
                next_note = next_note.enharmonic()
            if "#" in next_note.name:
                if flats:
                    next_note = next_note.enharmonic()
                if not flats and not sharps:
                    sharps = True
            if "b" in next_note.name:
                if sharps:
                    next_note = next_note.enharmonic()
                if not flats and not sharps:
                    flats = True
            index += 1
            n += 1
            spelling.append(next_note)
            
    return tuple(spelling)

#CHORD FUNCTIONS

#Takes a chord symbol (a string) and returns a dictionary of info about the chord, including a string of intervals
#Desperately needs refactoring
def parse_symbol(symbol):

    data = {}

    symbol = symbol.replace(" ","")

    root = re.match(constants.NOTE_REGEX_NONEND,symbol)
    if not root:
        raise ValueError("No valid root note.")

    root = root.group()

    symbol = symbol.replace(root,"")

    data["root"] = root

    #triad ifs
    if re.match(constants.MAJ_TRIAD_REGEX,symbol):
        quality = "Major"
        intervals = "M3 P5"
    elif re.match(constants.MIN_TRIAD_REGEX,symbol):
        quality = "Minor"
        intervals = "m3 P5"
    elif re.search(constants.AUG_TRIAD_REGEX,symbol):
        quality = "Augmented"
        intervals = "M3 A5"
    elif re.match(constants.DIM_TRIAD_REGEX,symbol):
        quality = "Diminished"
        intervals = "m3 D5"
    elif re.search(constants.POWER_CHORD_REGEX,symbol):
        quality = "5"
        intervals = "P5"
    elif re.search(constants.HALF_DIM_REGEX,symbol):
        quality = "Half diminished"
        intervals = "m3 D5 m7"
    elif re.search(constants.SUS_2_REGEX,symbol):
        quality = "Suspended 2"
        intervals = "M2 P5"
    elif re.search(constants.SUS_4_REGEX,symbol):
        quality = "Suspended 4"
        intervals = "P4 P5"
    else:
        quality = "Major"
        intervals = "M3 P5"

    #7
    if re.search(constants.MAJ_SEVEN_REGEX,symbol):
        intervals += " M7"    
    elif "7" in symbol:
        if quality == "Diminished":
            intervals += " D7"
        else:
            intervals += " m7"

    #9
    if re.search(constants.ADD_NINE_REGEX,symbol):
        intervals += " M2"
    elif re.search(constants.MAJ_NINE_CHORD_REGEX,symbol):
        intervals += " M7 M2"
    elif re.search(constants.NINE_CHORD_REGEX,symbol):
        if quality == "Diminished":
            intervals += " D7 M2"
        else:
            if "M7" not in intervals:
                intervals += " m7"
            intervals += " M2"

    #11
    if re.search(constants.MAJ_ELEVEN_REGEX,symbol):
        intervals = intervals.replace("M3","P4")
        intervals += " M2 M7"
    elif re.search(constants.ELEVEN_REGEX,symbol):
        if quality == "Minor":
            if "M7" not in intervals:
                intervals += " m7"
            intervals += " M2 P4"
        else:
            intervals = intervals.replace("M3","P4").replace("m3","P4")
            if "M7" not in intervals:
                if quality == "Diminished":
                    intervals += " D7"
                else:
                    intervals += " m7"
            intervals += " M2"
    
    #13
    if re.search(constants.MAJ_13_REGEX,symbol):
        intervals += " M7 M2 M6"
    elif re.search(constants.THIRTEEN_REGEX,symbol):
        if "M7" not in intervals:
            intervals += " m7"
        if quality == "Minor":
            intervals += " M2 P4 M6"
        intervals += " M2 M6"

    #extensions
    if re.search(constants.FLAT_9_REGEX,symbol):
        intervals = intervals.replace("M2","m2")
        intervals += " m2"

    if re.search(constants.SHARP_9_REGEX,symbol):
        intervals = intervals.replace("M2","A2")
        intervals += " A2"

    if re.search(constants.ADD_4_REGEX,symbol):
        intervals += " P4"
    
    if "#11" in symbol or "#4" in symbol:
        intervals += " A4"
    
    if "b5" in symbol:
        intervals = intervals.replace("P5","D5")
        intervals += " D5"
    
    if "#5" in symbol:
        intervals = intervals.replace("P5","A5")
        intervals += " A5"
    
    if re.search(constants.FLAT_6_REGEX,symbol):
        intervals = intervals.replace("M6","m6")
        intervals += " m6"

    elif "6" in symbol:
        intervals += " M6"

    if "alt" in symbol:
        intervals += " m2 m6"

    data['quality'] = quality
    data["intervals"] = intervals

    return data
    











