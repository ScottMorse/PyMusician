from pymusician.notate import _timesignature, _tempo, _clef, _staff

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

class Tempo(_tempo._Tempo):

    def __init__(self,bpm):
        super().__init__(bpm)
    
    @property
    def bpm(self):
        return self._bpm
    
    @bpm.setter
    def bpm(self,bpm):
        if not isinstance(bpm,(int,float)):
            raise ValueError("Tempo bpm value must be a number.")
        if bpm <= 0:
            raise ValueError("Tempo bpm must be positive.")
        self._bpm = bpm
        self._spb = 60 / bpm
        
    # seconds per beat
    @property
    def spb(self):
        return self._spb
    
class Clef(_clef._Clef):

    def __init__(self, clef_name, C4_position=None, clef_type=None):
        return super().__init__(clef_name, C4_position=C4_position, clef_type=clef_type)
    
    # string ("treble","bass","soprano",etc.)
    @property
    def clef_name(self):
        return self._clef_name
    
    # string ("F","G","C",etc.)
    @property
    def clef_type(self):
        return self._clef_type
    
    # int representing where C4 is, 0 being the position just below the staff bottom line
    @property
    def C4_position(self):
        return self._C4_position

class Staff(_staff._Staff):

    def __init__(self, key_sig='C', time_sig=TimeSignature(4, 4), starting_measures=1, bpm=60):
        return super().__init__(key_sig, time_sig, starting_measures, bpm)

    # A pymusician major Mode instance representing the key signature
    @property
    def key_mode(self):
        return self._key_mode
    
    # The root note given ('C', 'Bb', etc.)
    @property
    def key_sig(self):
        return self._key_sig

    # A TimeSignature instance
    @property
    def time_sig(self):
        return self._time_sig

    @property
    def measures(self):
        return self._measures

    # Add empty measure to end
    def append_measure(self):
        self._append_measure()
    
    # Insert empty measure at index
    def insert_measure_before(self,index):
        self._insert_measure_before(index)
    
    # Delete measure at index
    def delete_measure_at(self,index):
        self._delete_measure_at(index)
    
    # Add note to end, creates new measure if no room
    def append_note(self,note):
        self._append_note(note)

    # Clear measures between two indices, end exclusive
    def clear_selected_measures(self,start,end):
        self._clear_selected_measures(start,end)
    
    # Delete selected measures between two indices, end exclusive
    def delete_selected_measures(self,start,end):
        self._delete_selected_measures(start,end)