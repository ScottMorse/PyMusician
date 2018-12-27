# PyMusician by Scott Morse
## Version 1.0.2

## Latest in version
<a href="#version-history">Version History</a>
* Added code comments to __init__.py and utils.py
* Note class static methods such as `.note_from_values` and `.note_from_frequency` have been updated to allow passing optional rhythm and octave(for just `.note_from_values`) values into them, where they could not be before.
* Fixed bug where the `prefer` parameter for `.note_from_hard_pitch` made no effect on the result.

## Quick reference:
* Classes: <a href="#the-note-class">Note</a>, <a href="#the-interval-class">Interval</a>,<a href="#the-mode-class">Mode</a>,<a href="#the-chord-class">Chord</a>
* <a href="#pitchletter-reference">Pitch/letter values</a>
* <a href="#rhythm">Rhythm flags</a>
* <a href="#creating-a-basic-interval">Interval flags</a>
* <a href="#supported-mode-names">Mode names</a>

# **The Goal of PyMusician**

This is a python package for representing musical structures.  Its features have less to do with audio file production/management, and more with analysis and composition.  However, the concepts represented here could be combined with other music/audio related code to make sophisticated musical projects.

PyMusician isn't meant to be a stand-alone interface or notation program, but its purpose is to be able to automate all the music-theory related data that would go into such applications.

## Notes for non-musicians

The concepts in this package will be mostly foreign to anyone that hasn't studied common Western music theory.  The package most likely won't be useful to non-musicians.  However, I will try to give some explanation as to what this package is.  

All the music you hear in daily life has structure to it that can be analyzed with the practice of music theory.  Even *Mary Had a Little Lamb* and *Twinkle Twinkle Little Star* have definite structures that can be described in the distance of pitch (frequency, represented by note names like "C" and "B flat") and time (represented by the concept of "rhythm") between each note of the song. 

Groups of notes can be analyzed as larger structures, which can be analyzed between each other as even larger structures, all the way up to the analysis of an entire piece of music.

Music theory is much like programming itself, having many abstract concepts, but grounded in concrete data.  It is often called "the codification of music," so it's no wonder it can be translated into Python or any other programming language.  

The definitions and syntax of music theory itself come from an artistic point of view, yet the structures they represent are concrete: specific clusters of frequencies of air vibration (notes) and measurements of time (rhythm, beats per minute).  A musician does not talk about writing 440 Hz in a piece of music.  Instead we use the name "A4."  It is our code.

PyMusician's purpose is to create representations of these structures, from fundamental to complex, as objects of classes, and to allow a two-way street for both the analysis of this kind of data, and the creation of it.

# Getting started
## Prerequisites
You need an installation of Python 3.6 or higher.  To make use of this package, you should have a strong grasp of Python's object-oriented programming and a strong grasp on common Western music theory.
## Installation
PyMusician is now part of the PyPI community of python packages.  It's name is 'pymusician' for installation/importing.  It's easy to install
PyMusician with a simple pip command from your terminal:

```
$ pip install pymusician
```
Don't forget to make sure your pip version matches the command for Python version you are using.  (You may need to use a command like `pip3`, `pip3.7`, etc.)

# **General Concepts:**
If you have not used PyMusician before, it is important to read and learn about each class and function, as many core values and ideas of this code reappear in other sections, especially the properties and methods of the Note class.

## A4:
`A4` is a variable available in pymusician that represents the frequency for the note A4 in Hz.  By default, it is set to 440.  It can be set to a different number value simply by reassigning it.

```python
import pymusician
pymusician.A4 = 442
```
This will globally affect the rest of the code, by affecting any situation where frequency is calculated, such as the <a href="#frequency">frequency property</a> of a Note object.  This is the only value in the main that has global consequences within the code you are writing.
```python
import pymusician
pymusician.Note("A",4).frequency #440
pymusician.A4 = 442
pymusician.Note("A",4).frequency #442
```

# **The Note Class**
## The simplest objects:
An object from the Note class represents a pitched note (support for rests on the way).  The only required argument is the note name.  

A note name should just be a string of the common name for the note, such as "A","A#", "Bb", etc.  

A generally unlimited number of sharps/flats is technically allowed with accurate effects to the object's pitch-related values, though notes like this is are not generally not encouraged in PyMusician (or music in general).

Invalid note names will raise a `ValueError`.

```python
from pymusician import Note

A = Note("A")
Bb = Note("Bb")
Es = Note("E#")
Fbb = Note("Fbb") # technically possible
Gssss = Note("G####") # also technically possible...
```

A Note's name can be accessed as a string through `self.name.`
```python
Bb.name # 'Bb'

Gssss.name # 'G####'
```

## **Pitch and Letter Values:**

<a href="#pitchletter-reference">Pitch/letter value reference</a>

The two most basic attributes of a Note are its 'pitch' and 'letter'.  Both are integers, and both have nothing to do with specificity of octave (a separate property called hard_pitch deals with a value given on octave, read on).

## Pitch
The property `self.pitch` represents a relative value for a Note's pitch.  This starts at **0 for C natural**.  C#/Db then has the pitch 1, and D has 2 (Ebb or C## would also have this pitch), etc.  The range of pitch values is 0 to 11 (11 equivalent to B).  This is *not* octave-sensitive (see <a href="#hard-pitch">octave</a> and <a href="#hard-pitch">hard pitch</a>).

```python
from pymusician import Note

Note("C").pitch # 0

Note("C#").pitch # 1

Note("Db").pitch # 1

Note("D").pitch # 2

Note("Dbb").pitch # 0
```

## Letter

The property `self.letter` assigns an integer value for a Note's alphabetical letter, which similarly starts at **0 for C natural**.  Any Note using the same initial letter has the same letter value (C#,C##,Cb,Cbb all have 0).  The range of letter values is 0 to 6 (6 for the letter B).

```python
from pymusician import Note

C = Note("C")
Cs = Note("C#")
Db = Note("Db")
D = Note("D")

C.pitch # 0

C.letter # 0 

Cs.pitch # 1 

Cs.letter # 0

Db.pitch # 1

Db.letter # 1

D.pitch # 2

D.letter # 1

```
## **Pitch/Letter Reference:**
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
<span id="octave"></span>
## **Octave**

The second argument for a Note object is optional and denotes its octave value, which should be set to an integer.  Octave numbering is the same as common practice (Scientific Pitch Notation), 4 representing the middle octave, and octaves change at the note *C natural*.

It is possible to set the octave value after instantiating a Note.

Access the integer with `self.octave.`  If none is set, returns None

```python
from pymusician import Note

C4 = Note("C",4)

A = Note("A")
A.octave  # None

A.octave = 4
A.octave # 4

Gb0 = Note("Gb",0)

Bn1 = Note("B",-1)
```

## Hard Pitch

If a Note object's <a href="#octave">octave</a> value has been set, then the object has a property at `self.hard_pitch` that represents a concrete pitch value for the note represented by an integer.  **C0** is used as the basis, having a `hard_pitch` of 0, and `hard_pitch` values rise or fall by the half step from there.

If no `octave` has been set, returns None.

```python
from pymusician import Note

C0 = Note("C",0)

C0.hard_pitch # 0


C4 = Note("C",4)

C4.hard_pitch # 48


B3 = Note("B",3)

B3.hard_pitch # 47


Db4 = Note("Db",4)

Db4.hard_pitch # 49


_A4 = Note("A", 4)

_A4.hard_pitch # 57


F = Note("F")

F.hard_pitch # None
```

## **Rhythm**

The rhythm parameter is the third parameter (optional) for a Note.  This may be the first more alien-looking nomenclature, but with practice in using pymusician, it will make sense.  Finale users may find the system of numbering rhythm qualities familiar.

The rhythm is set by a string of flags.  The first flag determines the kind of rhythm.  The longest base rhythm is a double whole note, represented by the character "0"(zero), and the shortest is a 512th note, represented by "10".  Here is a list of base rhythms with their respective flags:
```
|------------|-------|
|   Rhythm   |  Flag |
|------------|-------|
|Double whole|  "0"  |
|    Whole   |  "1"  |
|    Half    |  "2"  |
|   Quarter  |  "3"  |
|    8th     |  "4"  |
|    16th    |  "5"  |
|    32nd    |  "6"  |
|    64th    |  "7"  |
|   128th    |  "8"  |
|   256th    |  "9"  |
|   512th    |  "10" |
|------------|-------|
```

The next possible flag is a dot.  Add "." or even multiple "."'s after the first flag to make a rhythm dotted, or doubly dotted, or triply dotted, etc.  This will make an effect on the value of the rhythm, covered later.

Finally, a "t" can be added to make a note a common 3:2 triplet.  This also actively effects the value of the rhythm's length.

The rhythm parameter is set in the third parameter when initializing an object, or later by assigning `self.rhythm` the correct flags.  

Examples (much needed):

```python
from pymusician import Note

#Middle C as a quarter note
#rhythm flags as the third op. parameter
C4q = Note("C",4,"3")

#Middle C as a dotted half note
C3h = Note("C",4,"2.")

#Ab as an eighth note (no octave)
Ab4e = Note("Ab",None,"4")

#F#2 as a sextuplet
Fs2sxt = Note("F#",2,"5t")

#E as a doubly dotted half note
E = Note("E")
E.rhythm = "2.."
```

Once the rhythm flags are set, `self.rhythm` returns an **object** acting like sub-object of the Note.  It has these properties:
* `rhythm.value` The length of the rhythm measured in **512th notes**
* `rhythm.flags` The original flags string
* `rhythm.num` The number from the flags
* `rhtyhm.dots` The number of dots in the rhythm
* `rhythm.triplet` True/False if rhythm is a triplet

```python
from pymusician import Note

C = Note("C")
C.rhythm = "3"
# a quarter note

C.rhythm.value # 128

C.rhythm = "3t"
C.rhythm.value # returns 85.3333... for the length of a quarter triplet
C.rhythm.triplet # True
C.rhythm.dots # 0

C.rhythm = "3."
C.rhythm.value # returns 192.0 for the length of a dotted quarter
C.rhythm.dots # 1
C.rhythm.triplet # False

```
## **Other Note class properties and methods**
As PyMusician grows, its classes will have more and more of the most useful properties and methods to have on hand.

## Pitch offset:

The property at `self.pitch_offset` is a simple integer representing how offset the relative pitch of the note is from its natural sibling.  For example, any natural notes have a pitch offset of 0, sharp notes have a pitch offset of 1, and flat notes have a pitch offset of -1.  A double sharp note has an offset of 2, and likewise a double flat has an offset of -2.

```python
from pymusician import Note

A = Note("A")
A.pitch_offset # 0

G = Note("G")
G.pitch_offset # 0

As = Note("A#")
As.pitch_offset # 1

Ab = Note("Ab")
Ab.pitch_offset # -1

Gs = Note("G#")
Gs.pitch_offset # 1

Gb = Note("Gb")
Gb.pitch_offset # -1

Bss = Note("B##")
Bss.pitch_offset # 2

Ebb = Note("Ebb")
Ebb.pitch_offset # -2

```

## Frequency

This property returns a float of the standard frequency for a note in Hz.  This will return None if there is no octave set for an object, because there is no specific pitch for a note without it.  If the global constant <a href="#a4">A4</a> is reassigned a new number, the basis for every frequency will be affected.

```python
import pymusician

pymusician.A4 

note_A4 = pymusician.Note("A",4)

note_A4.frequency # 440.0

note_A5 = pymusician.Note("A",5)

note_A5.frequency # 880.0

pymusician.A4 = 442 # reassign global A4

note_A4.frequency # 442.0

note_A5.frequency # 884.0
``` 
## **Methods**
## enharmonic()

A musician familiar with the term 'enharmonic' will recognize the usefulness of having this method and will hopefully be glad that it is written here.  

When this method is called on a Note object, it returns a new Note object that is the equivalent enharmonic to the original note.  This returns a new object *<span>w</span>ithout* affecting the original object in place.

By default, this will always convert a single sharp-note into a single-flat note, or any multi-sharp or multi-flat note into either a natural note or a single-sharp or single-flat note.

The method has two optional parameters to help customize the way this can be used, which can be useful if iterating it on several notes with certain needs.  
### Prefer
The first parameter is called 'prefer'.  By default, it is set to None, but if using, it should be set to "#" or "b".  Setting either of these will force the method to only return sharp or flat notes.  

This means that A# with a prefer of "#" will not convert to Bb but remain in place, and likewise, Bb will not convert to A# if prefer is set to "b". 

Abbb with a prefer of "b" will have a guaranteed conversion to Gb, and with a prefer of "#" will conver to F#.  

This finds use in situations of multi-sharp/flat notes or manual transposition, when all notes should fit a certain pattern to match a mode.
### Gross
The second optional parameter is called 'gross', because it deals with unpopular notes that are, however, often needed.  By default, this parameter is set to False, but can be set to True.

If True, this means that the notes B#, Cb, E#, and Fb as fair game as any other natural or single-sharp/flat note.  C will conver to B#, B will convert to Cb, E will convert to Fb, and F will convert to E#.  This may find its most common use when dealing with keys such as F#/Gb major.

```python
from pymusician import Note

Ds = Note("D#")
Eb = Ds.enharmonic() # successfully assigns Note("Eb") to variable Eb

Bbbb = Note("Bbbb")
Ab = Bbbb.enharmonic("b") # prefer set to 'b' guarantees Ab to return
Gs = Bbbb.enharmonic("#") # prefer set to '#' guarantees G# to return

F = Note("F")
F.enharmonic() # returns the same F natural
Es = F.enharmonic(None,True) # no preference of #/b, but allows gross
# ^ This now returns E# instead of F natural.

#A stranger situation to see the workings of this method:
Ass = Note("A##")
B = Ass.enharmonic() # reduces A double sharp to B natural
Cb = Ass.enharmonic().enharmonic(None,True) #returns B, then Cb
B = Ass.enharmonic().enharmonic("#",True) #returns B instead of Cb, preference of '#' negating the possibility of a flat

```
In general, you will probably most often use this function with no arguments simply to convert simple sharp/flat notes and reduce multi-sharp/flats.

## \_\_add_\_ & \_\_sub_\_
<a href="#note---interval-__add__--__sub__">Adding and subtracting Interval objects</a>

The Note class has adding and subtracting methods, which are used in tandum with the Interval class. Adding or subtracting an Interval object to a Note object returns a new Note object at that interval distance higher or lower.  Read more in the documentation for the <a href="#the-interval-class">Interval class</a>.

## **Static Methods**
The main purpose of the Note class's static methods is to allow the possibility to create instances of Note objects in different ways.

## Note.from_values(letter,pitch,octave=None,rhythm=None)

This method allows for the creation of a Note object from the <a href="#pitchletter-reference">letter and pitch values</a> (both integers) that are normally assigned a note object in normal construction. 

Keep in mind that this method only returns a simple object with no octave or rhythm, though these values can be set to an object after its creation.

Optional octave and rhythm arguments can be supplied.

```python
from pymusician import Note

C = Note.from_values(0,0) # C natural
Cs = Note.from_values(0,1) # C sharp
B = Note.from_values(6,11) # B natural
Bb = Note.from_values(6,10) # B flat
As = Note.from_values(5,10) # A sharp
A = Note.from_values(5,9,4,"3t") # A natural, octave 4, quarter triplet
```

## Note.from_hard_pitch(hard_pitch,prefer=None,rhythm=None)

Read earlier about **hard pitch** to understand the value required for this method's first argument.  It should be an integer representing the same hard_pitch that an octave-valued note is assigned.  

The optional 'prefer' parameter works similarly to the 'prefer' parameter in the `enharmonic()` method.  By default, this method returns sharp notes instead of flat, unless prefer is set to "b".

```python
from pymusician import Note

A4 = Note.from_hard_pitch(57) # A octave 4

C4 = Note.from_hard_pitch(48) # C octave 4

C0 = Note.from_hard_pitch(0) # C octave 0

Cs0 = Note.from_hard_pitch(1) # C sharp (sharp by default)

Db0 = Note.from_hard_pitch(1,'b') #prefer set to 'b' returns Db instead of C sharp

```
## Note.from_frequency(frequency,prefer=None,rhythm=None)
This is a very similar method to <a href="#notefrom_hard_pitchhard_pitchprefernone">`Note.from_hard_pitch`</a>, except taking a Hz value for the note.  The global constant <a href="#a4">A4</a> also will affect this method in the same way it affects any other <a href="#frequency">frequency</a>-related data.  

Since frequency values are usually not whole numbers, this method will round the given Hz to the closest accurate note frequency.  This may prove useful if this code is used alongside audio analysis.

Like `Note.from_hard_pitch`, it returns sharp notes by default, but the second optional parameter can be set to 'b' for flat notes.
```python
from pymusician import Note

A4 = Note.from_frequency(440) # A octave 4

Gs4 = Note.from_frequency(415) # G sharp octave 3, frequency is close enough

Ab4 = Note.from_frequency(415,'b') # Ab octave 3, frequency is close enough

A3 = Note.from_frequency(220) # A octave 3
```

*This class sets the foundation for the rest of PyMusician.*

# **The Interval Class**

Instances from the Interval class represent a pure interval value representing a distance between notes based on common practice nomenclature.

## Creating a basic Interval

The Interval constructor takes two arguments, the first being a string of flags to represent the basic interval, and the second being an optional value to displace an interval by a number of octaves (integer).

The flags are meant to be intuitive to those familiar with common interval names.  The flags should be a single string with two characters, the first representing the interval quality, and the second representing the interval size.  

The quality flag should be 'M' for major, 'm' for minor, 'P' for perfect, 'A' for augmented, and 'D' for diminished.  (Lowercase forgiven for 'P','A', or 'D')

The second flag should be the interval size, '1' for unison, '2' for second, etc. up to 7th.  Using '8' will work for a single octave, but in general, use the 'displace' parameter for intervals greater than an octave (read on).

This will look like 'm2' for a Minor 2nd, 'M3' for a Major 3rd, 'P4' (or 'p4' is forgiven) for Perfect 4th, 'A4' for Augmented Fourth, 'D5' (or 'd5') for Diminished 5th, etc.

Invalid names of intervals will raise `ValueError`'s.  This would include perfect 3rds, major 4ths, etc. Any interval can be augmented or diminished, so no errors will be raised for these.

```python
from pymusician import Interval

half_step = Interval('m2')

whole_step = Interval('M2')

minor_third = Interval('m3')

major_third = Interval('M3')

aug_third = Interval('A3') # successfully returns enharmonic equivalent to perfect 4th

per_fourth = Interval('P4')
```
In the rare case that an interval needs to be doubly/triply (or more) augmented or diminished, add '.' ' s after the 'A' or 'D' flag.
```python
from pymusician import Interval

doubly_augmented_fourth = Interval('A.4')
triply_diminished_fifth = Interval('D..5')
```

Here are examples that use the 'displace' optional parameter (default 0) to increase the number of octaves added to the interval.

```python
from pymusician import Interval

perfect_octave1 = Interval('P8')
perfect_octave2 = Interval('P1',1) #this represents the same interval

minor_9th = Interval('m2',1)

major_13th = Interval('M6',1)

dim7_and_two_octaves = Interval('D7',2)
```

## **Why have these objects?**

The most useful purpose for regular Interval objects like these is to combine in with the <a href="#the-note-class">Note</a> class's magic methods.

## Note +/- Interval (\_\_add\_\_ & \_\_sub\_\_)
These are methods that original in the Note class.  Simply add an Interval object to a Note object (Note object must come first), and receive a Note object at that distance higher, or subtract to descend by the Interval.

```python
from pymusician import Note, Interval

C4 = Note("C",4)

maj_2nd = Interval("M2")

maj_14th = Interval("M7",1)

octave = Interval("P8")

new_note_D4 = C4 + maj_2nd #creates Note("D",4)

new_note_D5 = new_note_D4 + octave #creates Note("D",5)

new_note_C3 = C4 - octave #creates Note("C",3)

new_note_B5 = C4 + maj_14th #creates Note("B",5)
```

## **Interval properties**

## self<span></span>.diff

The diff property returns an integer representing how many half steps long the distance of the interval is.  It would be 0 for perfect unison (`'p1'`), 1 for minor 2nd, etc.

## self<span></span>.letter_diff

The letter_diff property returns an integer representing how many letters change by an interval.  For example, all 2nds step in alphabetic letter by 1, regardless of quality, all 3rds change letter by 2, and so on.

## self<span></span>.name

This returns a more visually appealing name for the interval.  This would be a string such as `"Major 2nd"` for an `'M2'` interval, `"Major 13th"` for a major 6th displaced by one octave, and `"Perfect 4th plus 2 octaves"` for a perfect fourth displaced by two octaves.  This is mainly for convenience, though the \_\_repr\_\_ for Interval objects is also clear if one is familiar with the flags used in the initializer.

## **Static methods**
## Interval.from_notes(note_obj1,note_obj2)

This is a way to receive an Interval object from the distance between two Note objects.  If both Note objects have octave values, it will return an interval specific to their octave and pitch distance.  If one or neither have octave values, it will treat the first note as ascending to the second.

```python
from pymusician import Note, Interval

C4 = Note("C",4)
A4 = Note("A",4)

maj_6th = Interval.from_notes(C4,A4) # returns Interval('M6')

C2 = Note("C",2)

two_octaves = Interval.from_notes(C2,C4) # returns Interval('P1',2)

Bb = Note("Bb")
F = Note("F")

per_5th = Interval.from_notes(Bb,F) # returns Interval('P5')

per_4th = Interval.from_notes(F,Bb) # returns Interval('P4')
```

*There is certainly more to come with this class, especially in interval analysis.*

# **The Mode Class**

The Mode class is a very intuitive and simple class for a musician to deal with.

## Creating a Mode
To create a new Mode instance, all one needs is the root and mode name.  The root note can either be a string note name, or a <a href="#the-note-class">Note</a> object.  Below is a <a href="#supported-mode-names">reference</a> of Mode names.

```python
from pymusician import Note, Mode

cmaj = Mode("C","major")

C = Note("C")

cmaj = Mode(C, "ionian")

amin = Mode("A","minor")
```
## **Mode properties**

### Root
`self.root` simply returns the <a href="#the-note-class">Note</a> object for root of the mode.  Even if a string was passed originally for the root note, the property will be a Note instance.

### Mode
`self.mode` is simply the mode name, like "major", "minor."

### Name
`self.name` is a name combining the root and mode name ("A major")

## Spelling
This is the main purpose of the Mode class.  `self.spelling` is a list of Note objects that spell the Mode.  However, you can **iterate over a Mode instance itself** to iterate over its spelling for you, allowing you to treat the Mode itself like a list in iteration.  Also, **indexing the Mode instance** will index the spelling, and the **len()** of the Mode object is the length of its spelling.

```python
from pymusician import Note, Mode

d_harm_min = Mode("D","harmonic minor")

d_harm_min.spelling # List of Note objects: D E F G A Bb C#

#print every note name of the mode
for note in d_harm_min.spelling:
    print(note.name)

#equivalent to the previous lines of code
for note in d_harm_min:
    print(note.name)

d_harm_min[6] # Note("C#")

len(d_harm_min) # 7
```

## **Supported Mode Names**
#### Diatonic/common
* major, ionian
* minor, aeloian
* harmonic minor
* melodic minor
* dorian
* phrygian
* lydian
* mixolydian
* locrian
#### Pentatonic/blues
* major pentatonic
* minor pentatonic
* blues, minor blues
* major blues
#### Modes of melodic minor
* dorian flat 2
* lydian sharp 5
* lydian dominant
* mixolydian flat 6
* locrian sharp 2
* altered, super locrian
#### Symmetrical
* chromatic
* whole tone
* whole-half diminished, whole-half octatonic
* half-whole diminished, half-whole octatonic
* augmented




## *Custom Modes*
As of the moment, there is not support for custom modes within the Python, but the package's modes are found in a file called modes.json in the package's folder **/pymusician/data/modes.json**.

For now, if you want to add or edit your modes, open this json, and add your mode's name as a key to thes first object with an array of the steps of the mode as its value.  Make sure to include the step that returns to the root at the end. Like this:

```json
[
    {
        "ionian": [2,2,1,2,2,2,1],
        "major": "ionian1",
        "YOUR CUSTOM MODE": [2,1,2,1,2,2,2],
```

To clarify what is happening in this file, the modes with array values set the steps of a main mode (such as 2 for whole step, 1 for half step, 3 for minor 3rd/augmented 2nd).  The modes with string values refer to a parent mode and the scale degree from which the step pattern starts.

The Mode class will attempt to spell your mode in the best way that it can, but if your mode has an irregular step pattern that requires specific letter spellings, optionally add your mode to the second object of modes.json as well, with a "letter spelling" array, which corresponds to how many alphabetical letters each step should change.  For example, diatonic modes have letter spellings of [1,1,1,1,1,1,1,1], because letters always run strictly alphabetically in diatonic modes.

```json
[
    {
        "ionian": [1,1,1,1,1,1,1],
        "major": "ionian1",
        "YOUR CUSTOM MODE": [1,1,1,1,2,1,1],
```
As of now, many common modes are supported, and most users will most likely use mainly diatonic, harmonic/melodic minor, and pentatonic/blues modes, which are all fully supported.  Read the reference above for the names to use for them.  More support for custom modes will be sure to come with PyMusician.

# **The Chord Class**

The Chord class represents chords based on the common lead sheet symbol nomenclature.

Chord naming and spelling has various differing opinions in practice and is sometimes debated.  In PyMusician, a symbol reflecting what would be commonly seen in "lead music notation" is used to instantiate a Chord.  PyMusician does the best job that it can to parse the symbol it is given and spell the chord in the most accurate sense that can be derived from the symbol.

If you are familiar with lead sheet symbols, try simply passing it whatever chord symbol that you are comfortable with.

Keep in mind that chords with very strange and uncommon symbols may not behave as expected, especially if it is a symbol that should never see the light of day on a professional sheet of music ("Abb5(no3)(#9)(add9)13(b5)sus").  On an unrelated note, does anyone know of a name that rhymes with "Gone Sevens?" (not the actor)

This class is in the most infantile stage of all the classes here, and there is much more to come with different ways of creating and analyzing chords than from just lead sheet symbols.

## Create a Chord

To create a Chord, simply pass it a string of a chord symbol.  There are no set-in-stone rules, as PyMusician uses rigorous regular expressions to determine the chord.  Don't sweat things like parentheses except in cases where it may confuse the root of the chord ("Ab5" and "A(b5)" will be different chords).

```python

from pymusician import Chord

Amaj = Chord("A") # A major triad

Gbmin7 = Chord("Gbm7") # Gb minor 7

Csmin = Chord("C#-") # C# minor triad

Fb13 = Chord("Fb13") # Fb dominant 13

GmM7 = Chord("Gm(maj7)") # G minor (major 7th)

Bsus = Chord("Bsus4") # B suspended 4

Eb7b13s9 = Chord("Eb7b13#9") # E dominant, flat 13, sharp 9
```

Feel free to let me know of any chord spelling bugs that occur from the symbol parser, if you are sure that the spelling should be different. I have written hundreds of assertion tests to test the spellings of most commonly seen chord symbols, but there may still be some bugs in the cracks.

Keep in mind that there are many chord symbol practices, and though several options are supported by PyMusician, you may just need to try a slightly different symbol.

Support for slash chords (inversions) is coming soon!

## Chord Properties

### Symbol

`self.symbol` refers to the original symbol string used when making the chord.

### Root
`self.root` is a <a href="#the-note-class">Note</a> object of the root of the chord.

### Quality
`self.quality` is a triadic or base quality given to the chord as a string, such as "Major", "Minor", "Augmented", "Diminished", "5"(for 'power chords'), etc.

### Intervals
After the chord's root, quality, and extensions are parsed in initialization, `self.intervals` is a string of interval flags (such as used in the <a href="#the-interval-class">Interval</a> class) separated by spaces, such as "M3 P5" for a major triad.

### **Spelling**
`self.spelling`, like the <a href="#spelling">Mode</a> property, is a list spelling Note instances that make up the chord, including the root.  Also, like in a Mode instance, iterating over the Chord object itself is the same as iterating over its spelling property.  

You can also index or get the len() of a Chord instance directly to get a specific note from the spelling or the length of the number of notes represented.  Keep in mind that the index of the note you are searching for may not always be predicatable in chords with many extensions, though the root and triad will almost always be the first three indices [root,(third),(fifth)].

```python
from pymusician import Note, Chord

G13 = Chord("G13")

for note in G13.spelling:
    print(note.name)

#same as above code
for note in G13:
    print(note.name)

G13[0] # Note("G")
G13[1] # Note("B")
G13[2] # Note("D")
G13[3] # Note("F")
G13[4] # Note("A")
G13[5] # Note("E")

len(G13) # 6
```
## A note about 13 chords
In the most strict definition, a 13 chord contains an entire heptatonic scale worth of notes in it, including some kind of 11th/4th.  Some would argue that a dominant 13th chord should automatically then include a #11.  I have ommitted this, since in practice I believe this is not used strictly enough to always be included, though I understand why it is often argued.  In PyMusician, minor 13th chords do contain a natural 11, but any major quality 13 chords do not automatically include 11 or #11, so include it with a '#11' tag in the symbol ("G13#11").

# Concluding Thoughts

## What's coming in the future:
Many of these tools I have created in prototype projects of this package, but need to be redone and refined before releasing:
* Rests
* Time signatures
* BPM
* Concept of measures
* Transposition function
* Concept of a key, boolean function to determine membership to a key
* More Chord/Interval tools (including inversions)
* Clefs
* Staff position of Note objects based on clef/instrument transposition

## Version History
* #### 1.0.2
    * Added code comments to __init__.py and utils.py
    * Note class static methods such as `.note_from_values` and `.note_from_frequency` have been updated to allow passing optional rhythm and octave(for just `.note_from_values`) values into them, where they could not be before.
    * Fixed bug where the `prefer` parameter for `.note_from_hard_pitch` made no effect on the result.
* #### 1.0.1
    * <small>Fixed error in the Note method .enharmonic() when the Note object has rhythm value
    * Chord and Mode objects can be directly indexed and have a length with len(), referencing their spelling property</small>
* #### 1.0.0-b
    - <small>Released</small>

<br></br>
*For now, this concludes PyMusician's main tools. This project is in its early stages, and much more is to come.  This started as a single beginner's Python file that I used when I first started programming in order to practice applying musical concepts I knew well to new programming concepts I was learning, and now it is my main project that I plan to use in tandum with many more of my future projects.  I know there are a few other similar packages out there, but I thought I'd share mine for the public as well.  Thank you for reading, and have fun with this.*

*-Scott Morse*