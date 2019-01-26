from numpy import log2

TIME_DIVISIONS = [
    1,2,4,8,16,32,64,128,256,512
]

RHYTHM_NAMES = {
    1024: "double whole",
    512: "whole",
    256: "half",
    128: "quarter",
    64: "8th",
    32: "16th",
    16: "32nd",
    8: "64th",
    4: "128th",
    2: "256th",
    1: "512th"
}

class _TimeSignature:

    def __init__(self,top_number,bottom_number):
        if not (isinstance(top_number,(int,float)) and
                isinstance(bottom_number,int)):
            raise ValueError("Time signature must be intialized via two numbers (top, bottom).")
        if bottom_number not in TIME_DIVISIONS:
            raise ValueError("Bottom time signature number must be a common power of 2: (1,2,4,8,16,32,64,128,256,512)")
        if top_number < 1:
            raise ValueError("Top time signature number must be 1 or greater.")

        self._top = top_number
        self._bottom = bottom_number

        self._beat_len = tuple(RHYTHM_NAMES.keys())[int(log2(bottom_number)) + 1]

        self._gets_beat = RHYTHM_NAMES[self._beat_len]

        self._measure_len = self._beat_len * self._top