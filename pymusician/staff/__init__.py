from pymusician.staff import _timesignature

class TimeSignature(_timesignature._TimeSignature):

    #intialized with the two numbers as seen on sheet music: (4,4) for common time, (3,4) for waltz
    def __init__(self,top_number,bottom_number):
        super().__init__(top_number,bottom_number)

    #numeric
    @property
    def top_number(self):
        return self._top
    
    #numeric
    @property
    def bottom_number(self):
        return self._bottom

    #returns string name of the rhythm that gets the beat
    @property
    def gets_beat(self):
        return self._gets_beat

    #the length of a single beat in 512th notes (numeric)
    @property
    def beat_len(self):
        return self._beat_len

    #the total length of a measure in 512th notes (numeric)
    @property
    def measure_len(self):
        return self._measure_len
    
    def __repr__(self):
        return f'<TimeSignature {self.top_number}/{self.bottom_number}>'
    
    #All comparisons
    def __eq__(self,other):
        return _timesignature.timesignatures_eq(self,other)
    def __ne__(self,other):
        return _timesignature.timesignatures_ne(self,other)