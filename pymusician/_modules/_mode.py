PARENT_SPELLINGS = {
    "ionian": [[2,2,1,2,2,2,1], [1,1,1,1,1,1,1]], # [pitch spelling, letter spelling]
    "major pentatonic": [[2,2,3,2,3], [1,1,2,1,2]],
    "major blues": [[2,1,1,3,2,3], [1,0,1,2,1,2]],
    "harmonic minor": [[2,1,2,2,1,3,1], [1,1,1,1,1,1,1]],
    "melodic minor": [[2,1,2,2,2,2,1], [1,1,1,1,1,1,1]],
    "chromatic": [[1,1,1,1,1,1,1,1,1,1,1,1], None], # [pitch spelling, (use auto letter spelling)]
    "whole tone": [[2,2,2,2,2,2], None],
    "whole-half diminished": [[2,1,2,1,2,1,2,1], None],
    "half-whole diminished": [[1,2,1,2,1,2,1,2], None],
    "augmented": [[3,1,3,1,3,1], [1,1,2,0,2,1]]
}

MODES = {
    "ionian": ["ionian",1], # refers to a parent mode at a scale degree
    "major": ["ionian",1],
    "dorian": ["ionian",2],
    "phrygian": ["ionian",3],
    "lydian": ["ionian",4],
    "mixolydian": ["ionian",5],
    "aeolian": ["ionian",6],
    "minor": ["ionian",6],
    "locrian": ["ionian",7],
    "harmonic minor": ["harmonic minor",1],
    "major pentatonic": ["major pentatonic",1],
    "minor pentatonic": ["major pentatonic",5],
    "major blues": ["major blues",1],
    "minor blues": ["major blues",6],
    "blues": ["major blues",6],
    "melodic minor": ["melodic minor",1],
    "dorian flat 2": ["melodic minor",2],
    "lydian sharp 5": ["melodic minor",3],
    "lydian dominant": ["melodic minor",4],
    "mixolydian flat 6": ["melodic minor",5],
    "locrian sharp 2": ["melodic minor",6],
    "super locrian": ["melodic minor",7],
    "altered": ["melodic minor",7],
    "whole-half octatonic": ["whole-half diminished",1],
    "half-whole octatonic": ["half-whole diminished",1],
    "whole-half diminished": ["whole-half diminished",1],
    "half-whole diminished": ["half-whole diminished",1],
    "chromatic": ["chromatic",1],
    "whole tone": ["whole tone",1],
    "augmented": ["augmented",1]
}

class _Mode:

    def __init__(self,root,mode_quality,pitch_spelling=None,letter_spelling=None):
        from pymusician import Note

        if root.__class__.__name__ == "Note":
            self._root = root
        else:
            try:
                root = Note(root.capitalize())
                self._root = root
            except:
                raise ValueError("Mode root should be a Note object or a valid note name (str).")

        offset = 0

        if not pitch_spelling:
            try:
                mode_data = MODES[mode_quality]
                parent = PARENT_SPELLINGS[mode_data[0]]
                offset = mode_data[1] - 1
                pitch_spelling = parent[0]
                letter_spelling = parent[1]
            except KeyError:
                raise ValueError("Default mode not found. Include pitch_spelling for custom modes.")
        else:
            if not isinstance(pitch_spelling,(list,tuple)):
                raise ValueError("Mode pitch_spelling must be a list or tuple of integers.")
            for item in pitch_spelling:
                if not isinstance(item,int):
                    raise ValueError("Mode pitch_spelling must be a list or tuple of integers.")
                if item < 0 or item > 11:
                    raise ValueError("Mode pitch_spelling values must be between 0 and 11")

            if letter_spelling:
                if not isinstance(letter_spelling,(list,tuple)):
                    raise ValueError("Mode letter_spelling must be a list or tuple of integers.")
                if len(letter_spelling) != len(pitch_spelling):
                    raise ValueError("Mode letter_spelling must match length of its pitch spelling.")
                for item in letter_spelling:
                    if not isinstance(item,int):
                        raise ValueError("Mode letter_spelling must be a list or tuple of integers.")
                    if item < 0 or item > 6:
                        raise ValueError("Mode letter_spelling values must be between 0 and 6")
        
        self._mode = mode_quality
        self._name = self.root.name + " " + mode_quality

        self._offset = offset
        self._pitch_spelling = pitch_spelling
        self._letter_spelling = letter_spelling
        
        ############### SPELLING #################

        spelling = [root]

        next_pitch = root.pitch
        next_letter = root.letter
        i = offset

        n = 1

        flats = "b" in root.name
        sharps = "#" in root.name

        spelling_len = len(pitch_spelling)

        for step in pitch_spelling:
            if n == spelling_len:
                break
            if i == spelling_len:
                i -= spelling_len
            
            next_pitch += pitch_spelling[i]

            #correct for circular pitch pattern
            if next_pitch < 0:
                next_pitch += 12
            if next_pitch > 11:
                next_pitch -= 12

            # either use given letter spelling or add 1 to letter
            if letter_spelling:
                next_letter += letter_spelling[i]
            else:
                next_letter += 1

            # correct for circular letter pattern
            if next_letter < 0:
                next_letter += 7
            if next_letter > 6:
                next_letter -= 7

            if letter_spelling:
                next_note = Note.from_values(next_letter,next_pitch)

            # logic for automatic letter spelling:
            else:
                next_note = Note.from_values(next_letter,next_pitch)
                if len(next_note.name) > 2:
                    next_note = next_note.enharmonic()
                if next_note.name in ("B#","Cb","E#","Fb"):
                    next_note = next_note.enharmonic()
                if "#" in next_note.name:
                    if flats:
                        next_note = next_note.enharmonic()
                    if not flats and not sharps:
                        sharps = True
                if "b" in next_note.name:
                    if sharps:
                        next_note = next_note.enharmonic()
                    if not flats and not sharps:
                        flats = True

            spelling.append(next_note)
            i += 1
            n += 1

        self._spelling = tuple(spelling)

# COMPARISON FUNCTIONS

def modes_eq(mode1,mode2):
    if len(mode1) != len(mode2):
        return False

    try:
        for i in range(len(mode1)):
            if mode1[i] != mode2[i]:
                return False
    except IndexError:
        return False
    return True

def modes_ne(mode1,mode2):
    return not (mode1 == mode2)