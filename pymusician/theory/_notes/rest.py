from pymusician._bases.notelike import NoteLike

class Rest(NoteLike):
    
    def __init__(self,rhythm_ratio):
        super.__init__(rhythm_ratio)

    @property
    def pitch_val(self):
        return None