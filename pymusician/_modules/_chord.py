import re

class _Chord:

    def __init__(self,symbol):
        from pymusician import Note, Interval

        self._symbol = symbol

        data = parse_symbol(symbol)
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

NOTE_REGEX_NONEND = r'^[A-Ga-g]([#]+|[b]*)'

#triadic
MAJ_TRIAD_REGEX = r'^maj$|^major$|^M$|$'

MIN_TRIAD_REGEX = r'-|m$|m[^a]'

AUG_TRIAD_REGEX = r'[Aa]ug(mented)?|\+'

DIM_TRIAD_REGEX = r'o|°|[Dd]im(inished)?'

POWER_CHORD_REGEX = r'^5|no3'

HALF_DIM_REGEX = r'ø|[Hh]alf[Dd]im(inished)?'

SUS_2_REGEX = r'sus(pended)?2'

SUS_4_REGEX = r'sus(pended)?(4)?'

#seventh
MAJ_SEVEN_REGEX = r'(M|[Mm]aj(or)?)7'

ADD_NINE_REGEX = r'[Aa]dd[92]|^2|[^s]2|/9'

MAJ_NINE_CHORD_REGEX = r'M9|[Mm]aj(or)?9'

NINE_CHORD_REGEX = r'^9|[^b#/6]9'

#eleven
MAJ_ELEVEN_REGEX = r'(M|[Mm]aj(or)?)11'

ELEVEN_REGEX = r'^11|[^#bd]11'

#thirteen
MAJ_13_REGEX = r'(M|[Mm]aj(or)?)13'

THIRTEEN_REGEX = r'^13|[^#b]13'

FLAT_9_REGEX = r'b[92]'

SHARP_9_REGEX = r'#[92]'

ADD_4_REGEX = r'[Aa]dd(4|11)'

FLAT_6_REGEX = r'(b|flat)(6|13)'

#Takes a chord symbol (a string) and returns a dictionary of info about the chord, including a string of intervals
#Desperately needs refactoring
def parse_symbol(symbol):

    data = {}

    symbol = symbol.replace(" ","")

    root = re.match(NOTE_REGEX_NONEND,symbol)
    if not root:
        raise ValueError("No valid root note.")

    root = root.group()

    symbol = symbol.replace(root,"")

    data["root"] = root

    #triad ifs
    if re.match(MAJ_TRIAD_REGEX,symbol):
        quality = "Major"
        intervals = "M3 P5"
    elif re.match(MIN_TRIAD_REGEX,symbol):
        quality = "Minor"
        intervals = "m3 P5"
    elif re.search(AUG_TRIAD_REGEX,symbol):
        quality = "Augmented"
        intervals = "M3 A5"
    elif re.match(DIM_TRIAD_REGEX,symbol):
        quality = "Diminished"
        intervals = "m3 D5"
    elif re.search(POWER_CHORD_REGEX,symbol):
        quality = "5"
        intervals = "P5"
    elif re.search(HALF_DIM_REGEX,symbol):
        quality = "Half diminished"
        intervals = "m3 D5 m7"
    elif re.search(SUS_2_REGEX,symbol):
        quality = "Suspended 2"
        intervals = "M2 P5"
    elif re.search(SUS_4_REGEX,symbol):
        quality = "Suspended 4"
        intervals = "P4 P5"
    else:
        quality = "Major"
        intervals = "M3 P5"

    #7
    if re.search(MAJ_SEVEN_REGEX,symbol):
        intervals += " M7"    
    elif "7" in symbol:
        if quality == "Diminished":
            intervals += " D7"
        else:
            intervals += " m7"

    #9
    if re.search(ADD_NINE_REGEX,symbol):
        intervals += " M2"
    elif re.search(MAJ_NINE_CHORD_REGEX,symbol):
        intervals += " M7 M2"
    elif re.search(NINE_CHORD_REGEX,symbol):
        if quality == "Diminished":
            intervals += " D7 M2"
        else:
            if "M7" not in intervals:
                intervals += " m7"
            intervals += " M2"

    #11
    if re.search(MAJ_ELEVEN_REGEX,symbol):
        intervals = intervals.replace("M3","P4")
        intervals += " M2 M7"
    elif re.search(ELEVEN_REGEX,symbol):
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
    if re.search(MAJ_13_REGEX,symbol):
        intervals += " M7 M2 M6"
    elif re.search(THIRTEEN_REGEX,symbol):
        if "M7" not in intervals:
            intervals += " m7"
        if quality == "Minor":
            intervals += " M2 P4 M6"
        intervals += " M2 M6"

    #extensions
    if re.search(FLAT_9_REGEX,symbol):
        intervals = intervals.replace("M2","m2")
        intervals += " m2"

    if re.search(SHARP_9_REGEX,symbol):
        intervals = intervals.replace("M2","A2")
        intervals += " A2"

    if re.search(ADD_4_REGEX,symbol):
        intervals += " P4"
    
    if "#11" in symbol or "#4" in symbol:
        intervals += " A4"
    
    if "b5" in symbol:
        intervals = intervals.replace("P5","D5")
        intervals += " D5"
    
    if "#5" in symbol:
        intervals = intervals.replace("P5","A5")
        intervals += " A5"
    
    if re.search(FLAT_6_REGEX,symbol):
        intervals = intervals.replace("M6","m6")
        intervals += " m6"

    elif "6" in symbol:
        intervals += " M6"

    if "alt" in symbol:
        intervals += " m2 m6"

    data['quality'] = quality
    data["intervals"] = intervals

    return data

#! TODO
def chord_from_notes(*notes,root=None):
    from pymusician import Note

    notes = list(notes)
    #root can be provided or by default is first note provided

    if not root:
        root = notes[0]
        del notes[0]
    if isinstance(root,str):
        try:
            root = Note(root)
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
                note = Note(note)
            except:
                raise ValueError("Invalid note passed to Chord.from_notes")
        elif not note.__class__.__name__ == "Note":
            raise ValueError("Invalid note passed to Chord.from_notes")
        if note.name == root.name:
            continue
        intvls.append(Interval.from_notes(root,note))