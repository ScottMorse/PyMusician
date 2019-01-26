import re

INT_FLAG_REGEX = r'^[Mm][2367]$|[ADad][.]*[1-8]$|^[Pp][1458]$'

INTVLS = {
    "1": 0, "2": (1,2),
    "3": (3,4), "4": 5,
    "5": 7, "6": (8,9),
    "7": (10,11)
}

INTVL_NAMES = ("unison","2nd","3rd","4th","5th","6th","7th","octave")

class _Interval:

    def __init__(self,flags,displace=0):
        flags = flags.strip()
        if not isinstance(flags, str):
            raise ValueError("Interval flags (first argument) should be a string.")
        if not re.match(INT_FLAG_REGEX,flags):
            raise ValueError("Invalid interval flags.  (see documentation)")
        if not isinstance(displace,int):
            raise ValueError("Displacement value should be a positive integer or 0(default).")
        if displace < 0:
            raise ValueError("Displacement value should be a positive integer or 0(default).")
        self._flags = flags
        self._displace = displace
        self._diff = intvl_diff(flags,displace)
        self._letter_diff = int(self._flags[-1]) - 1
        self._name = intvl_namer(self)

#Returns an integer value which describes the distance represented by an Interval
def intvl_diff(flags,_displace):
    intvl_quality = flags[0]
    adder_dots = len(flags) - 2
    intvl_type = flags[-1]
    if intvl_type == '8':
        intvl_type = '1'
        _displace += 1

    base_diff = INTVLS[intvl_type]
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
        base = INTVL_NAMES[int(intvl._flags[-1]) - 1]
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

def intvl_from_notes(note_obj1,note_obj2):
    from pymusician import Interval, Note

    if type(note_obj1) is not Note or type(note_obj2) is not Note:
        raise ValueError("Invalid Note object passed.")

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
    
    expected_pitch = INTVLS[base_flag]

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
    
    intvl = Interval(flags,displace)
    return intvl