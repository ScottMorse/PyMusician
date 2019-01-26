import json
import os

BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR,"../data/modes.json")
with open(FILE_PATH) as j:
    loaded = json.load(j)

MODES = loaded[0]
MODE_LETTER_SPELLINGS = loaded[1]

class _Mode:

    def __init__(self,root,mode):
        from pymusician import Note
        if root.__class__.__name__ == "Note":
            self._root = root
        else:
            try:
                self._root = Note(root.capitalize())
            except:
                raise ValueError("Mode root should be a Note object or a valid note name (str).")
        if mode not in MODES:
            raise KeyError("Mode not found.  View the modes json to see/add modes.")
        self._mode = mode
        self._name = self.root.name + " " + mode
        self._spelling = mode_speller(self.root,self.mode)

#returns a tuple of Note objects for the given mode
def mode_speller(root,mode):
    from pymusician import Note

    spelling = [root]

    if type(MODES[mode]) is str:
        parent_name = MODES[mode][:len(MODES[mode])-1]
        offset = int(MODES[mode][-1]) - 1
    elif type(MODES[mode]) is list:
        parent_name = mode
        offset = 0
    else:
        raise ValueError("Invalid Mode pattern. (Check modes json)")
    parent = MODES[parent_name]
    for item in parent:
        if type(item) is not int:
            raise ValueError("Invalid Mode pattern. (Check modes json)")
    
    next_pitch = root.pitch
    next_letter = root.letter
    index = offset
    n = 1
    flats = False if "b" not in root.name else True
    sharps = False if "#" not in root.name else True
    if parent_name in MODE_LETTER_SPELLINGS:
        for step in parent:
            if index == len(parent):
                index -= len(parent)
            if n == len(parent):
                break
            next_pitch += parent[index]
            if parent_name in MODE_LETTER_SPELLINGS:
                next_letter += MODE_LETTER_SPELLINGS[parent_name][index]
            else:
                next_letter += 1
            if next_pitch < 0:
                next_pitch += 12
            elif next_pitch > 11:
                next_pitch -= 12
            if next_letter < 0:
                next_letter += 7
            elif next_letter > 6:
                next_letter -= 7
            if parent_name in MODE_LETTER_SPELLINGS:
                next_note = Note.from_values(next_letter,next_pitch)
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
            index += 1
            n += 1
    else:
        flats = False if "b" not in root.name else True
        sharps = False if "#" not in root.name else True
        for step in parent:
            if index == len(parent):
                index -= len(parent)
            if n == len(parent):
                break
            next_pitch += parent[index]
            next_letter += 1
            if next_pitch < 0:
                next_pitch += 12
            elif next_pitch > 11:
                next_pitch -= 12
            if next_letter < 0:
                next_letter += 7
            elif next_letter > 6:
                next_letter -= 7
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
            index += 1
            n += 1
            spelling.append(next_note)
            
    return tuple(spelling)
