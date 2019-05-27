import re
from enum import Enum

import pymusician._utils.guards as grd

class NoteData:
  
    def __init__(self,pitch_val,letter_val):
        self._pitch_val = pitch_val
        self._letter_val = letter_val

    @property
    def pitch_val(self):
        return self._pitch_val

    @pitch_val.setter
    def pitch_val(self,num):
        self._pitch_val = num
    
    @property
    def letter_val(self):
        return self._letter_val

class NoteEnum(Enum):

    C = NoteData(0,0)
    D = NoteData(2,1)
    E = NoteData(4,2)
    F = NoteData(5,3)
    G = NoteData(7,4)
    A = NoteData(9,5)
    B = NoteData(11,6)

    @staticmethod
    def get_by_name(name):
        grd.validate_note_name(name)

        letter = name[0].upper()

        for note in NoteEnum:
            if note.name == letter:
                note_data = note.value

        if '#' in name:
            note_data.pitch_val += len(name) - 1
        elif 'b' in name:
            note_data.pitch_val -= len(name) - 1

        return note_data