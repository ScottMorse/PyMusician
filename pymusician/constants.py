import json
import os

BASE_DIR = os.path.dirname(__file__)

NOTE_REGEX = r'^[A-Ga-g]([#]*$|[b]*$)'

NOTE_REGEX_NONEND = r'^[A-Ga-g]([#]+|[b]*)'

RHYTHM_REGEX = r'^(10|[0-9])[\.]*[t]?$'

NOTES = ["C","D","E","F","G","A","B"]

NOTE_VALUES = {
    "C": (0,0), "D": (1,2),
    "E": (2,4), "F": (3,5),
    "G": (4,7), "A": (5,9),
    "B": (6,11),
}

RHYTHM_VALUES = [
    1024,512,256,128,
    64,32,16,8,4,2,1,
]

GROSS_ROOTS = {"B":"Cb","C":"B#","E":"Fb","F":"E#"}
NON_NATURAL = (1,3,6,8,10)

INT_FLAG_REGEX = r'^[Mm][2367]$|[ADad][.]*[1-8]$|^[Pp][1458]$'

INTVLS = {
    "1": 0, "2": (1,2),
    "3": (3,4), "4": 5,
    "5": 7, "6": (8,9),
    "7": (10,11)
}

INTVL_NAMES = ("unison","2nd","3rd","4th","5th","6th","7th","octave")

BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR,"data/modes.json")
with open(FILE_PATH) as j:
    loaded = json.load(j)

MODES = loaded[0]
MODE_LETTER_SPELLINGS = loaded[1]

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