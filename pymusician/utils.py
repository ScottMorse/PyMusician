import pymusician
from pymusician import constants
from numpy import log2
import re

#TODO refactoring speller functions and possibly rethink how rhythm and interval flags are written/parsed.

###INTERVAL CLASS FUNCTIONS

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

def chord_from_notes(*notes,root=None):
    notes = list(notes)
    #root can be provided or by default is first note provided

    if not root:
        root = notes[0]
        del notes[0]
    if isinstance(root,str):
        try:
            root = pymusician.Note(root)
        except:
            raise ValueError("Invalid root note ")
    elif not root.__class__.__name__ == "Note":
        raise ValueError("Invalid note passed to Chord.from_notes")

    symbol = root.name
    intvls = []

    for i in range(len(notes)):
        note = notes[i]
        if isinstance(note,str):
            try:
                note = pymusician.Note(note)
            except:
                raise ValueError("Invalid note passed to Chord.from_notes")
        elif not note.__class__.__name__ == "Note":
            raise ValueError("Invalid note passed to Chord.from_notes")
        if note.name == root.name:
            continue
        intvls.append(pymusician.Interval.from_notes(root,note))

    


