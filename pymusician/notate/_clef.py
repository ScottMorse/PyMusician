CLEFS = {
    "treble": [-1,"G"],
    "suboctave treble": [-1, "G8vb"],
    "bass": [10, "F"],
    "soprano": [1,"C"],
    "mezzo-soprano": [3,"C"],
    "alto": [5,"C"],
    "tenor": [7,"C"],
    "baritone": [9,"C"],
    "french violin": [-3,"G"],
    "neutral": [None, "Neutral"]
}

class _Clef:

    def __init__(self,clef_name,C4_position=None,clef_type=None):

        if not isinstance(clef_name,str):
            raise ValueError("Clef name must be a string.")
        
        if not C4_position is None:
            if not isinstance(C4_position,int):
                raise ValueError("Positon of C4 must be an int (0 being the position just below bottom line)")
            if not isinstance(clef_type,str):
                raise ValueError("Clef type must be a string.")
            self._C4_position = C4_position
            self._clef_type = clef_type
        else:
            try:
                clef_data = CLEFS[clef_name]
            except KeyError:
                raise ValueError("Invalid clef name. Include the two optional arguments (C4_position, clef_type) for a custom clef.")
            self._C4_position = clef_data[0]
            self._clef_type = clef_data[1]

        self._clef_name = clef_name

        
        