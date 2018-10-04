# PyMusician by Scott Morse
## Version 1.0.0-beta

A python package for representing musical structures.  The features of the musictools module have less to do with audio file production/management, and more with analysis and composition.  However, the concepts represented here could be combined with other music/audio related code to make sophisticated musical projects.  The goal of Music Tools is to be versatile and intuitive to a musician-programmer with practice, representing musical concepts in a way musicians will find familiar, and leaving room to use the information in any way the user wishes, rather than creating any interfaces for programs such as sheet music notation directly.


# Getting started
## Prerequisites
You need an installation of Python 3.6 or higher.  PyMusician uses NumPy, but if your python library doesn't have it, the package will download it automatically.  To make use of this package, you should have a strong grasp of Python's object-oriented programming and a strong grasp on common Western music theory.
## Installation
PyMusician is now part of the PyPI community of python packages.  It's name is 'pymusician' for installation/importing.  It's easy to install
PyMusician with a simple pip command from your terminal:

```
$ pip install pymusician
```
Don't forget to make sure your pip version matches the command for Python version you are using.  (You may need to use a command like pip3, pip3.7, etc.)

# **General Concepts:**
If you have not used PyMusician before, it is important to read and learn about each class and function, as many core values and ideas of this code reappear in other sections, especially the properties and methods of the Note class.

## A4:
A4 is a constant available in pymusician that represents the frequency for the note A4 in Hz.  By default, it is set to 440.  It can be set to a different number value simply by reassigning it.

```python
>>> import pymusician
>>> pymusician.A4 = 442
```
This will globally affect the rest of the code, by affecting any situation where frequency is calculated, such as the frequency property of a Note object.  This is the only value in the main that has global consequences within the functions of pymusician.
```python
>>> import pymusician
>>> pymusician.Note("A",4).frequency #440
>>> pymusician.A4 = 442
>>> pymusician.Note("A",4).frequency #442
```

# **The Note Class**
## The simplest objects:
An object from the Note class represents a pitched note (support for rests on the way).  The only required argument is for a name.  

A note name should just be a string of the common name for the note, such as "A","A#", "Bb", etc.  

A generally unlimited number of sharps/flats is technically allowed with accurate affects to the object's pitch-related values, though notes like this is are not generally not encouraged in pymusician or music in general, and may behave strangely in instances of Intervals or Chords.

Invalid note names will raise a ValueError.

```python
from pymusician import Note

A = Note("A")
Bb = Note("Bb")
Es = Note("E#")
Fbb = Note("Fbb") # technically possible
Gssss = Note("G####") # also technically possible...
```

A Note's name can be accessed as a string through self.<span></span>name.
```python
Bb.name # 'Bb'

Gssss.name # 'G####'
```

## **Pitch and Letter Values:**

(after this information is a list of pitch and letter values for reference)

Two basic attributes of a Note that are given to it are it's 'pitch' and 'letter'.  Both are integers, and both have nothing to do with specificity of octave (a separate property called hard_pitch deals with a value given on octave, read on).

## Pitch
The property self.<span></span>pitch represents a relative value for a Note's pitch.  This starts at **0 for C natural**.  C#/Db then has the pitch 1, and D has 2 (Ebb or C## would also have this pitch), etc.  The range of pitch values is 0 to 11 (11 equivalent to B).

```python
from pymusician import Note

Note("C").pitch # 0

Note("C#").pitch # 1

Note("Db").pitch # 1

Note("D").pitch # 2

Note("Dbb").pitch # 0
```

## Letter

The property self.<span></span>letter assigns an integer value for a Note's alphabetical letter, which similarly starts at **0 for C natural**.  Differently than the pitch value, any Note using the same letter has the same letter value (C#,C##,Cb,Cbb all have 0).  The range of letter values is 0 to 6 (6 for the letter B).

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

Access the integer with self.<span></span>octave.  If none is set, returns None

```python
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

The rhythm parameter is set in the third parameter, or as optional parameter 'rhythm=' when initializing an object or after by assigning self.<span></span>rhythm the correct flags.  

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

After a rhythm is set, accessing the self.<span></span>rhythm property returns a dictionary of data about the rhythm.
The *['value']* key returns the length of the rhythm measured in **512th** notes.  *['dots']* returns the number of dots used in the flags.  *['triplet']* returns a Boolean for whether the rhythm is a triplet.  *['num']* returns the number used in the first flag.  Finally, *['flags']* returns the flags string originally used.  ***self.<span></span>rhythm['value']*** is perhaps the most useful of this data.

```python
from pymusician import Note

C = Note("C")
C.rhythm = "3"
# a quarter note

C.rhythm['value']
# returns 128, since a quarter is 128 512th notes long

C.rhythm = "3t"
C.rhythm['value']
# returns 85.3333.... for the length of a quarter triplet

C.rhythm = "3."
# returns 192 for the length of a dotted quarter

```
## **Other Note class properties and methods**
As PyMusician grows, its classes will have more and more of the most useful properties and methods to have on hand.

## Pitch offset:

The property at self.<span></span>pitch_offset is a simple integer representing how offset the relative pitch of the note is from its natural sibling.  For example, any natural notes have a pitch offset of 0, sharp notes have a pitch offset of 1, and flat notes have a pitch offset of -1.  A double sharp note has an offset of 2, and likewise a double flat has an offset of -2.

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

This property returns a float of the standard frequency for a note in Hz.  This will return None if there is no octave set for an object, because there is no specific pitch for a note without it.  If the global constant pymusician.A4 is reassigned a new number (see General Notes at top of this readme), the basis for every frequency will be affected.

```python
import pymusician

pymusician.A4 

note_A4 = pymusician.Note("A",4)

note_A4.frequency # 440.0

note_A5 = pymusician.Note("A",5)

note_A5.frequency # 880

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
The Note class has adding and subtracting methods, which are actually used in tandum with the Interval class. Adding or subtracting an Interval object to a Note object returns a new Note object at that interval distance higher or lower.  Read more in the documentation for the Interval class.

## **Static Methods**
The main purpose of the Note class's static methods is to allow the possibility to create instances of Note objects in different ways.
## Note.from_values(letter,pitch)

This method allows for the creation of a Note object from the letter and pitch values (both integers) that are normally assigned a note object in normal construction. (Read the previous section entitled **Pitch and Letter Values** to understand what these integers are)

Keep in mind that this method only returns a simple object with no octave or rhythm, though these values can be set to an object after its creation.

```python
from pymusician import Note

C = Note.from_values(0,0) # C natural
Cs = Note.from_values(0,1) # C sharp
B = Note.from_values(6,11) # B natural
Bb = Note.from_values(6,10) # B flat
As = Note.from_values(5,10) # A sharp
A = Note.from_values(5,9) # A natural
```

## Note.from_hard_pitch(hard_pitch,prefer=None)

Read earlier about **hard pitch** to understand the value required for this method's first argument.  It should be an integer representing the same hard_pitch that an octave-valued note is assigned.  

The optional 'prefer' parameter works similarly to the 'prefer' parameter in the *enharmonic()* method.  By default, this method returns sharp notes instead of flat, unless prefer is set to "b".

```python
from pymusician import Note

A4 = Note.from_hard_pitch(57) # A octave 4

C4 = Note.from_hard_pitch(48) # C octave 4

C0 = Note.from_hard_pitch(0) # C octave 0

Cs0 = Note.from_hard_pitch(1) # C sharp (sharp by default)

Db0 = Note.from_hard_pitch(1,'b') #prefer set to 'b' returns Db instead of C sharp

```
## Note.from_frequency(frequency,prefer=None)
This is a very similar method to Note.from_hard_pitch, except taking a Hz value for the note.  The global constant A4 also will affect this method in the same way it affects any other frequency-related data.  

Since frequency values are usually not whole numbers, this method will round the given Hz to the closest accurate note frequency.  This may prove useful if this code is used alongside audio analysis.

Like Note.from_hard_pitch, it returns sharp notes by default, but the second optional parameter can be set to 'b' for flat notes.
```python
from pymusician import Note

A4 = Note.from_frequency(440) # A octave 4

Gs4 = Note.from_frequency(415) # G sharp octave 3, frequency is close enough

Ab4 = Note.from_frequency(415,'b') # Ab octave 3, frequency is close enough

A3 = Note.from_hard_pitch(220) # A octave 3
```

*For now, this concludes the Note class.  It is chock full of data, since it sets the fundamental structure for the rest of PyMusician.*

# **The Interval Class**

Instances from the Interval class represent a pure interval value representing a distance between notes based on common practice nomenclature.

## Creating a basic Interval

The Interval constructor takes two arguments, the first being a string of flags to represent the basic interval, and the second being an optional value to displace an interval by a number of octaves (integer).

The flags are meant to be intuitive to those familiar with common interval names.  The flags should be a single string with two characters, the first representing the interval quality, and the second representing the interval size.  

The quality flag should be 'M' for major, 'm' for minor, 'P' for perfect, 'A' for augmented, and 'D' for diminished.  (Lowercase forgiven for 'P','A', or 'D')

The second flag should be the interval size, '1' for unison, '2' for second, etc. up to 7th.  Using '8' will work for a single octave, but in general, use the 'displace' parameter for intervals greater than an octave (read on).

This will look like 'm2' for a Minor 2nd, 'M3' for a Major 3rd, 'P4' (or 'p4' is forgiven) for Perfect 4th, 'A4' for Augmented Fourth, 'D5' (or 'd5') for Diminished 5th, etc.

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

## Why have these objects?

The most useful purpose for regular Interval objects like these is to combine in with the Note class's magic methods.

## Note +/- Interval (\_\_add\_\_ & \_\_sub\_\_)
These are methods that comes from the Note class.  Simply add an Interval object to a Note object (Note object must come first), and receive a Note object at that distance higher, or subtract to descend by the Interval.

```python
from pymusician import Note, Interval

C4 = Note("A",4)

maj_2nd = Interval("M2")

D4 = C4 + maj2nd #creates Note("D",4)

octave = Interval("P8")

D5 = D4 + octave #creates Note("D",5)

C3 = C4 - octave #creates Note("C",3)


```