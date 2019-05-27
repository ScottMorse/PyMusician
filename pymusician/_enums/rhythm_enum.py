import re
from enum import Enum
from math import isclose

import pymusician._utils.guards as grd

class Rhythm:
  
    def __init__(self, ratio, name, symbol):
        self._ratio = ratio
        self._name = name
        self._symbol = symbol

        self._count512 = ratio / 0.001953125

    @property
    def ratio(self):
        return self._ratio

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

    @property
    def count512(self):
        return self._count512

class RhythmEnum(Enum):
  
    DOUBLE_WHOLE = Rhythm(2, 'double whole', '𝅜')
    WHOLE = Rhythm(1, 'whole', '𝅝')
    HALF = Rhythm(0.5, 'half', '𝅗𝅥')
    QUARTER = Rhythm(0.25, 'quarter', '𝅘𝅥')
    EIGHTH = Rhythm(0.125, '8th', '𝅘𝅥𝅮')
    SIXTEENTH = Rhythm(0.0625, '16th', '𝅘𝅥𝅯')
    THIRTY_SECOND = Rhythm(0.03125, '32nd', '𝅘𝅥𝅰')
    SIXTY_FOURTH = Rhythm(0.015625, '64th', '𝅘𝅥𝅱')
    ONE_HUNDRED_TWENTY_EIGHTH = Rhythm(0.0078125, '128th', '𝅘𝅥𝅲')
    TWO_HUNDRED_FIFTY_SIXTH = Rhythm(0.00390625, '256th', '')
    FIVE_HUNDRED_TWELFTH = Rhythm(0.001953125, '512th', '')

    @staticmethod
    def get_by_ratio(ratio):
        grd.validate_rhythm_ratio(ratio)
        
        for rhythm in RhythmEnum:
            test_ratio = rhythm.value.ratio
            num_digits = len(str(test_ratio))

            if isclose(ratio,test_ratio,abs_tol=10**-(num_digits)):
                return rhythm.value

        return RhythmEnum.QUARTER.value

    @staticmethod
    def get_by_name(name):
        for rhythm in RhythmEnum:
            test_name = rhythm.value.name
            if re.match(test_name, name,re.IGNORECASE):
                return rhythm.value

        return RhythmEnum.QUARTER.value