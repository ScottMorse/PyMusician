# Official Documentation Site is Up!
# <a href="http://www.pymusician.com" target="_blank">www.pymusician.com</a>

# PyMusician 1.2.0
Author: Scott Morse

## Latest in version:&nbsp;&nbsp;<small>(<a href="#version-history">Version History</a>)</small>
&nbsp;&nbsp;&nbsp;&nbsp;*MAKE THE CORRECT DATE*

* Modes spelling algorithm refactored
* Support for custom modes with new optional parameters for Mode instances (see docs)
* Notes and intervals can be compared with all comparison operators
* Modes, chords, and time signatures can be compared with `==` and `!=`

# Getting started
## Prerequisites
You need an installation of Python 3.6 or higher.  To make use of this package, you should have a strong grasp of Python's object-oriented programming and a strong grasp on common Western music theory.
## Installation
PyMusician is now part of the Python Package Index.  It's name is `pymusician` for installation/importing.  It's easy to install
PyMusician with a simple `pip` command from your terminal:

```
$ pip install pymusician
```

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

## What's coming in the future:
Many of these tools I have created in prototype projects of this package, but need to be redone and refined before releasing:
* Rests
* BPM
* Concept of measures
* Transposition function
* Concept of a key, boolean function to determine membership to a key
* More Chord/Interval tools (including inversions)
* Clefs
* Staff position of Note objects based on clef/instrument transposition

## Version History
* #### 1.1.1&nbsp;&nbsp;&nbsp;&nbsp;<small>*January 26,2019*</small>
    * Non-breaking project restructure. New module structure, separated tests, and some more efficient class properties.  One uncaught unfinished Chord function removed.
* #### 1.1.0&nbsp;&nbsp;&nbsp;&nbsp;<small>*January 25,2019*</small>
    * TimeSignature class added for representation of basic but highly dynamic time signatures
    * The value of A4 is now protected.
    * Main classes all take named arguments instead of *args now
* #### 1.0.2&nbsp;&nbsp;&nbsp;&nbsp;<small>*December 27,2018*</small>
    * Added code comments to __init__.py and utils.py(deprecated)
    * Note class static methods such as `.note_from_values` and `.note_from_frequency` have been updated to allow passing optional rhythm and octave(for just `.note_from_values`) values into them, where they could not be before.
    * Fixed bug where the `prefer` parameter for `.note_from_hard_pitch` made no effect on the result.
* #### 1.0.1&nbsp;&nbsp;&nbsp;&nbsp;<small>*November 22, 2018*</small>
    * <small>Fixed error in the Note method .enharmonic() when the Note object has rhythm value
    * Chord and Mode objects can be directly indexed and have a length with len(), referencing their spelling property</small>
* #### 1.0.0-b&nbsp;&nbsp;&nbsp;&nbsp;<small>*October 8, 2018*</small>
    - <small>Released</small>

<br></br>
