import pymusician._utils.guards as grd
from pymusician._enums.rhythm_enum import RhythmEnum

class NoteLike(ABC):
  
    def __init__(self,rhythm_ratio = 1/4):
        self._rhythm = RhythmEnum.get_by_ratio(rhythm_ratio)
        
        super().__init__()

    @property
    def rhythm(self):
        return self._rhythm