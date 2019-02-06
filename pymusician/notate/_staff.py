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
