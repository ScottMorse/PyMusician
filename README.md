# PyMusician by Scott Morse
## Version 1.0.0-beta

A python package for representing musical structures.  The features of the musictools module have less to do with audio file production/management, and more with analysis and composition.  However, the concepts represented here could be combined with other music/audio related code to make sophisticated musical projects.  The goal of Music Tools is to be versatile and intuitive to a musician-programmer with practice, representing musical concepts in a way musicians will find familiar, and leaving room to use the information in any way the user wishes, rather than creating any interfaces for programs such as sheet music notation directly.


# Getting started
## Prerequisites
You need an installation of Python 3.6 or higher.  Music Tools uses NumPy, but if your python library doesn't have it, the package will download it automatically.  To make use of this package, you should have a strong grasp of Python's object-oriented programming and a strong grasp on common Western music theory.
## Installation
Music Tools is now part of the PyPI community of python packages.  It's name is 'musictools' for installation/importing.  It's easy to install
Music Tools with a simple pip command from your terminal:

```
$ pip install pymusician
```
Don't forget to make sure your pip version matches the command for Python version you are using.  (You may need to use a command like pip3, pip3.7, etc.)

# General Concepts:

## A4:
A4 is a constant available in pymusician that represents the frequency for the note A4 in Hz.  By default, it is set to 440.  It can be set to a different number value simply by reassigning it.

```
>>> import pymusician
>>> pymusician.A4 = 442
```
This will globally affect the rest of the code, by affecting any situation where frequency is calculated, such as the frequency property of a Note object.  This is the only value in the main that has global consequences within the functions of pymusician.
```
>>> import pymusician
>>> pymusician.Note("A",4).frequency #440
>>> pymusician.A4 = 442
>>> pymusician.Note("A",4).frequency #442
```

# The Note Class
## The simplest objects:
An object from the Note class represents a pitched note (support for rests on the way).  The only required argument is for a name.  

A note name should just be a string of the common name for the note, such as "A","A#", "Bb", etc.  

A generally unlimited number of sharps/flats is technically allowed with accurate affects to the object's pitch-related values, though notes like this is are not generally not encouraged in pymusician or music in general, and may behave strangely in instances of Intervals or Chords.

Invalid note names will raise a ValueError.
```
from pymusician import Note

A = Note("A")
Bb = Note("Bb")
Es = Note("E#")
Fbb = Note("Fbb") #technically possible...
Gssss = Note("G####") #also technically possible...
```

A Note's name can be accessed as a string through self.<span></span>name.
```
Bb.name
# 'Bb'

Gssss.name
# 'G####'
```

## Pitch and Letter Values:

(after this information is a list of pitch and letter values for reference)

Two basic attributes of a Note that are given to it are it's 'pitch' and 'letter'.  Both are integers, and both have nothing to do with specificity of octave (a separate property called hard_pitch deals with a value given on octave, read on).

## Pitch
The property self.<span></span>pitch represents a relative value for a Note's pitch.  This starts at **0 for C natural**.  C#/Db then has the pitch 1, and D has 2 (Ebb or C## would also have this pitch), etc.  The range of pitch values is 0 to 11 (11 equivalent to B).

```
from pymusician import Note

Note("C").pitch
# 0

Note("C#").pitch
# 1

Note("Db").pitch
# 1

Note("D").pitch
# 2

Note("Dbb").pitch
# 0
```

## Letter

The property self.<span></span>letter assigns an integer value for a Note's alphabetical letter, which similarly starts at **0 for C natural**.  Differently than the pitch value, any Note using the same letter has the same letter value (C#,C##,Cb,Cbb all have 0).  The range of letter values is 0 to 6 (6 for the letter B).

```
from pymusician import Note

C = Note("C")
Cs = Note("C#")
Db = Note("Db")
D = Note("D")

C.pitch
# 0
C.letter
# 0

Cs.pitch
# 1
Cs.letter
# 0

Db.pitch
# 1
Db.letter
# 1

D.pitch
# 2
# 1

```
## Pitch/Letter Reference:
Here is a list of note names with their respective pitch and letter values.
```
|-----------------------|
| name | pitch | letter |
|------|-------|--------|
|  C   |   0   |    0   |
|  C#  |   1   |    0   |
|  Db  |   1   |    1   |
|  D   |   2   |    1   |
|  D#  |   3   |    1   |
|  Eb  |   3   |    2   |
|  E   |   4   |    2   |
|  F   |   5   |    3   |
|  F#  |   6   |    3   |
|  Gb  |   6   |    4   |
|  G   |   7   |    4   |
|  G#  |   8   |    4   |
|  Ab  |   8   |    5   |
|  A   |   9   |    5   |
|  A#  |   10  |    5   |
|  Bb  |   10  |    6   |
|  B   |   11  |    6   |
|-----------------------|
```

## Octave

The second argument for a Note object is optional and denotes its octave value, which should be set to an integer.  Octave numbering is the same as common practice (Scientific Pitch Notation), 4 representing the middle octave, and octaves change at the note *C natural*.

It is possible to set the octave value after instantiating a Note.

Access the integer with self.<span></span>octave.  If none is set, returns None

```
from pymusician import Note

C4 = Note("C",4)

A = Note("A")
A.octave 
# None

A.octave = 4
A.octave
# 4

Gb0 = Note("Gb",0)

Bn1 = Note("B",-1)
```

## Hard Pitch

If a Note object's octave value has been set, then the object has a property at self.<span></span>hard_pitch that represents a concrete pitch value for the note represented by an integer.  **C0** is used as the basis, having a hard_pitch of 0, and hard_pitch values rise or fall by the half step from there.

If no octave has been set, returns None.

```
from pymusician import Note

C0 = Note("C",0)
C0.hard_pitch 
# 0

C4 = Note("C",4)
C4.hard_pitch 
# 48

B3 = Note("B",3)
B3.hard_pitch
# 47

Db4 = Note("Db",4)
Db4.hard_pitch
# 49

_A4 = Note("A", 4)
_A4.hard_pitch
# 57

F = Note("F")
F.hard_pitch
# None
```

