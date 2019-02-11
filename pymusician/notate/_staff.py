class _Staff:

    def __init__(self,
        key_sig="C",
        time_sig=None,
        starting_measures=1,
        bpm=60
    ):
        from pymusician import Mode
        from pymusician.notate import TimeSignature, Tempo

        if time_sig is None:
            time_sig = TimeSignature(4,4)
            
        if not type(time_sig) is TimeSignature:
            raise ValueError("Staff time_sig argument must be a TimeSignature instance.")
        if not isinstance(starting_measures,int):
            raise ValueError("Staff starting measures must be an integer of at least 1.")
        if starting_measures < 0:
            raise ValueError("Staff starting measures can't be negative.")
        
        try:
            self._key_mode = Mode(key_sig,"major")
        except:
            raise ValueError("Staff: invalid key given. Must be a note name (ex: 'C' or 'Bb' or 'F#')")
        try:
            self._tempo = Tempo(bpm)
        except:
            raise ValueError("Staff: invalid bpm given.")

        self._key_sig = key_sig
        self._time_sig = time_sig
        
        measures = [Measure(time_sig.measure_len) for measure in range(starting_measures)]

        self._measures = measures

    @property
    def measures(self):
        return self._measures
    
    @property
    def key_sig(self):
        return self._key_sig

    @property
    def key_mode(self):
        return self._key_mode

    @property
    def time_sig(self):
        return self._time_sig
    
    @property
    def tempo(self):
        return self._tempo

    def append_measure(self):
        self._measures.append(Measure())
    
    def insert_measure_before(self,index):
        self._measures.insert(index,Measure())
    
    def delete_measure_at(self,index):
        try:
            del self._measures[index]
        except IndexError:
            raise IndexError("No measure at such index.")
    

class Measure:

    def __init__(self,measure_len):
        self._notes = []
        self._space_filled = 0
        self._space_left = measure_len
        self._measure_len = measure_len

    # bool 
    @property
    def is_empty(self):
        return self._space_filled == 0
    
    # bool
    @property
    def is_full(self):
        return self._space_left == 0

    # number, rhythmic value filled measured in 512th notes
    @property
    def space_filled(self):
        return self._space_filled
    
    # number, rhythmic value left measured in 512th notes
    @property
    def space_left(self):
        return self._space_left

    # list of Note objects
    @property
    def notes(self):
        return self._notes

    def append_note(self,note):
        if note.__class__.__name__ not in ("Note","Rest"):
            raise ValueError("Only can add Note or Rest instances to a measure.")
        if not note.rhythm:
            raise ValueError("Note must have a rhythm value.")
        if note.rhythm.value + self._space_filled > self._measure_len:
            raise Exception("No space left in measure.")
        self._notes.append(note)
        self._space_filled += note.rhythm.value
        self._space_left -= note.rhythm.value

    def insert_note_before(self,index,note):
        if not isinstance(index,int):
            raise ValueError("Index must be an int.")
        if note.__class__.__name__ not in ("Note","Rest"):
            raise ValueError("Only can add Note or Rest instances to a measure.")
        if not note.rhythm:
            raise ValueError("Note must have a rhythm value.")
        if note.rhythm.value + self._space_filled > self._measure_len:
            raise Exception("No space left in measure.")
        self._notes.insert(index,note)
    
    def delete_note_at(self,index):
        if not isinstance(index,int):
            raise ValueError("Index must be an int.") 
        try:
            del self._notes[index]
        except IndexError:
            raise IndexError("No note at such index.")
            
    def clear_notes(self):
        self._notes = []