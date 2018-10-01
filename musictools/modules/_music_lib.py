import json

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

INT_FLAG_REGEX = r'^[Mm][2367]$|[ADad][.]*[1-7]$|^[Pp][145]$'

INTVLS = {
    "1": 0, "2": (1,2),
    "3": (3,4), "4": 5,
    "5": 7, "6": (8,9),
    "7": (10,11)
}

INTVL_NAMES = ("unison","2nd","3rd","4th","5th","6th","7th")

with open("musictools/site-packages/modes.json") as j:
    loaded = json.load(j)

MODES = loaded[0]
MODE_LETTER_SPELLINGS = loaded[1]

MAJOR_REGEX = r"maj(or)?|M"

MINOR_REGEX = r"m(in(or)?)?|-"

AUG_REGEX = r"[Aa]ug(mented)?|[\+]"

DIM_REGEX = r"[Dd]im(inished)?|°|o"

SUS_REGEX = r"[Ss]us(pended)?[^2]?"

HALF_REGEX = r"[Hh]alfdim(inished)?|ø|m(in(or)?)?7(\()?b5(\))?"

POWER_REGEX = r"(\()?5|[Nn]o(3|thi)rd(\))"

ALL_QUAL_REGEX = r"m(in(or)?)?|[Aa]ug(mented)?|[+]|[Dd]im(inished)?|°|o|[Hh]alfdim(inished)?|ø|m(in(or)?)?7(\()?b5(\))|(\()?5|[Nn]o(3|thi)rd(\))"

FLAT_2_REGEX = r"(\()(b|flat)[29](\))"

TWO_REGEX = r"(\()(add?[29]|2)(\))"

SHARP_9_REGEX = r"(\()?(#|sharp)9(\))?"

ADD_4_REGEX = r"(\()?add4(\))?"

SHARP_11_REGEX = r"(\()?#(11|4)(\))?"

FLAT_5_REGEX = r"(\()?(b|flat)5(\))?"

SHARP_5_REGEX = r"(\()?#5(\))?"

FLAT_6_REGEX = r"(\()?(b|flat)(6|13)(\))?"

SIX_REGEX = r"(\()?6(\))?"

SIX_NINE_REGEX = r"(\()?6(/)?9(\))?"

MAJ_7_REGEX = r"(\()?(maj(or)?|M)7(\))?"

PLAIN_7_REGEX = r"(\()?(dom(inant)?)?7(\))?"

MAJ_9_REGEX = r"(\()?(maj(or)?|M)9(\))?"

PLAIN_9_REGEX = r"(\()?9(\))?"

PLAIN_11_REGEX = r"(\()?11(\))?"

MAJ_13_REGEX = r"(\()?(maj(or)?|M)13(\))?"

PLAIN_13_REGEX = r"(\))?13(\))?"