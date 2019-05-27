import pymusician._utils.guards as grd

from pymusician._bases.notelike import NoteLike
from pymusician._enums.note_enum import NoteEnum

class Note(NoteLike):
  
    def __init__(self,name,octave = 4,rhythm_ratio = 1/4):
        name_data = NoteEnum.get_by_name(name)

        self._name = name
        self._octave = grd.validate_octave(octave)
        self._pitch_val = name_data.pitch_val
        self._letter_val = name_data.letter_val

        super().__init__(rhythm_ratio)

    @property
    def name(self):
        return self._name

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self,octave):
        self._octave = grd.validate_octave(octave)

    @property
    def pitch_val(self):
        return self._pitch_val
    
    @property
    def letter_val(self):
        return self._letter_val

    @property
    def description(self):
        return self._name + self._octave + ' ' + self._rhythm.name

    
    