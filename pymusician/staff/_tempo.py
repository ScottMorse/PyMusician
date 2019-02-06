class _Tempo:

    def __init__(self,bpm):

        if not isinstance(bpm,(int,float)):
            raise ValueError("Tempo bpm value must be a number.")
        if bpm <= 0:
            raise ValueError("Tempo bpm must be positive.")

        self._bpm = bpm
        self._spb = 60 / bpm # seconds per beat