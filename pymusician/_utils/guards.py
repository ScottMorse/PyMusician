import re

NOTE_REGEX = r'^[A-Ga-g]([#]*$|[b]*$)'

def validate_note_name(name):
    if not re.match(NOTE_REGEX,name):
        raise ValueError('Invalid note name provided.')
    return name

def validate_rhythm_ratio(ratio):
    try:
        return float(ratio)
    except:
        raise ValueError('Rhythm ratio must be a number')

def validate_octave(octave):
    try:
        return int(octave)
    except:
        raise ValueError('Octave value must be an integer')