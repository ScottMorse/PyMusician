import unittest
import musictools


class TestNoteClass(unittest.TestCase):

    def test_A4(self):
        self.assertEqual(musictools.A4,440)
    
    def test_set_A4(self):
        musictools.A4 = 442
        self.assertEqual(musictools.A4,442)

    def test_natural_note(self):
        note_A = musictools.Note("A")
        note_A = musictools.Note("a ")
        note_G = musictools.Note(" G")
        self.assertEqual(note_A.name, "A")
        self.assertEqual(note_G.name, "G")
        with self.assertRaises(ValueError):
            musictools.Note('H')   
    
    def test_accidentals(self):
        note_As = musictools.Note("A#")
        note_Bbb = musictools.Note("Bbb")
        note_Gss = musictools.Note("G##")
        note_Fb = musictools.Note("Fb")
        with self.assertRaises(ValueError):
            musictools.Note('Ab#')
            musictools.Note('E#b')
    
    def test_letter_value(self):
        self.assertEqual(musictools.Note("C").letter,0)
        self.assertEqual(musictools.Note("C#").letter,0)
        self.assertEqual(musictools.Note("Bb").letter,6)
        self.assertEqual(musictools.Note("Abb").letter,5)
    
    def test_pitch_value(self):
        self.assertEqual(musictools.Note("C").pitch,0)
        self.assertEqual(musictools.Note("Cb").pitch,11)
        self.assertEqual(musictools.Note("C#").pitch,1)
        self.assertEqual(musictools.Note("Db").pitch,1)
        self.assertEqual(musictools.Note("Bb").pitch,10)
        self.assertEqual(musictools.Note("Abb").pitch,7)
    
    def test_octave(self):
        self.assertEqual(musictools.Note("C").octave, None)
        self.assertEqual(musictools.Note("C",4).octave, 4)
        with self.assertRaises(ValueError):
            musictools.Note("C",1.1)
        with self.assertRaises(ValueError):
            musictools.Note("C","C")
    
    def test_rhythm_set(self):
        musictools.Note("C",4,"0t")
        dot_quarter = musictools.Note("D",5,"3.")
        sextuplet = musictools.Note("E",2,"5t")
        crazy = musictools.Note("Fbbb",-10,"7..t")
        with self.assertRaises(ValueError):
            musictools.Note("C",1,"4tt")
        with self.assertRaises(ValueError):
            musictools.Note("C",1,"11tt")
    
    def test_rhythm_val(self):
        musictools.Note("C",4,"0t").rhythm

        double_whole = musictools.Note("C",2,"0")
        self.assertEqual(double_whole.rhythm['value'],1024)

        five_twelth = musictools.Note("C",3,"10")
        self.assertEqual(five_twelth.rhythm['value'],1)

        dot_quarter = musictools.Note("D",5,"3.")
        self.assertEqual(dot_quarter.rhythm['value'],192)

        trip_quarter = musictools.Note("E",2,"3t")
        self.assertAlmostEqual(trip_quarter.rhythm['value'],85.3333333333333)
    
    def test_pitch_offset(self):
        note_As = musictools.Note("A#")
        note_C = musictools.Note("C")
        note_Gb = musictools.Note("Gb")
        note_G = musictools.Note("G")
        note_Ess = musictools.Note("E##")
        note_Bbb = musictools.Note("Bbb")
        note_Dss = musictools.Note("D##")
        self.assertEqual(note_As.pitch_offset,1)
        self.assertEqual(note_C.pitch_offset,0)
        self.assertEqual(note_Gb.pitch_offset,-1)
        self.assertEqual(note_G.pitch_offset,0)
        self.assertEqual(note_Ess.pitch_offset,2)
        self.assertEqual(note_Bbb.pitch_offset,-2)
        self.assertEqual(note_Dss.pitch_offset,2)

    def test_hard_pitch(self):
        C0 = musictools.Note("C",0)
        C1 = musictools.Note("C",1)
        Cn1 = musictools.Note("C",-1)
        C4 = musictools.Note("C",4)
        B3 = musictools.Note("B",3)
        B4 = musictools.Note("B",4)
        Db4 = musictools.Note("Db",4)
        A4 = musictools.Note("A",4)
        self.assertEqual(C0.hard_pitch,0)
        self.assertEqual(C1.hard_pitch,12)
        self.assertEqual(Cn1.hard_pitch,-12)
        self.assertEqual(C4.hard_pitch,48)
        self.assertEqual(B3.hard_pitch,47)
        self.assertEqual(B4.hard_pitch,59)
        self.assertEqual(Db4.hard_pitch,49)
        self.assertEqual(A4.hard_pitch,57)
    
    def test_frequency(self):
        A4 = musictools.Note("A",4)
        A3 = musictools.Note("A",3)
        A5 = musictools.Note("A",5)
        C4 = musictools.Note("C",4)
        B3 = musictools.Note("B",3)
        B4 = musictools.Note("B",4)
        Db4 = musictools.Note("Db",4)
        self.assertEqual(A4.frequency,440)
        self.assertEqual(A3.frequency,220)
        self.assertEqual(A5.frequency,880)
        self.assertAlmostEqual(C4.frequency,261.6,1)
        self.assertAlmostEqual(B3.frequency,246.9,1)
        self.assertAlmostEqual(B4.frequency,493.9,1)
        self.assertAlmostEqual(Db4.frequency,277.2,1)

    def test_from_values(self):
        C = musictools.Note.from_values(0,0)
        A = musictools.Note.from_values(5,9)
        Bs = musictools.Note.from_values(6,0)
        Fb = musictools.Note.from_values(3,4)
        Gbb = musictools.Note.from_values(4,5)
        Asss = musictools.Note.from_values(5,0)
        self.assertEqual(C.name,"C")
        self.assertEqual(A.name,"A")
        self.assertEqual(Bs.name,"B#")
        self.assertEqual(Fb.name,"Fb")
        self.assertEqual(Gbb.name,"Gbb")
        self.assertEqual(Asss.name,"A###")
        

    def test_enharmonic(self):
        C = musictools.Note("C")
        Bs = musictools.Note("B#")
        E = musictools.Note("E")
        Fb = musictools.Note("Fb")
        Dss = musictools.Note("D##")
        As = musictools.Note("A#")
        Bb = musictools.Note("Bb")
        Abbb = musictools.Note("Abbb")
        self.assertEqual(Bs.enharmonic().name,C.name)
        self.assertEqual(E.enharmonic(None,True).name,Fb.name)
        self.assertEqual(Fb.enharmonic().name,E.name)
        self.assertEqual(Dss.enharmonic().name,E.name)
        self.assertEqual(As.enharmonic().name,Bb.name)
        self.assertEqual(Bb.enharmonic().name,As.name)
        self.assertEqual(As.enharmonic("#").name,"A#")
        self.assertEqual(Bb.enharmonic("b").name,"Bb")
        self.assertEqual(Abbb.enharmonic("#").name,"F#")
        self.assertEqual(Abbb.enharmonic("b").name,"Gb")

    def test_from_hard_pitch(self):
        A4 = musictools.Note.from_hard_pitch(57)
        C0 = musictools.Note.from_hard_pitch(0)
        C4 = musictools.Note.from_hard_pitch(48)
        B3 = musictools.Note.from_hard_pitch(47)
        Db4 = musictools.Note.from_hard_pitch(49,prefer="b")
        Cs4 = musictools.Note.from_hard_pitch(49)
        self.assertEqual(A4.name,"A")
        self.assertEqual(C0.name,"C")
        self.assertEqual(C4.name,"C")
        self.assertEqual(B3.name,"B")
        self.assertEqual(Db4.name,"Db")
        self.assertEqual(Cs4.name,"C#")
        self.assertEqual(A4.octave,4)
        self.assertEqual(C0.octave,0)
        self.assertEqual(C4.octave,4)
        self.assertEqual(B3.octave,3)
        self.assertEqual(Db4.octave,4)
        self.assertEqual(Cs4.octave,4)

    def test_from_frequency(self):
        A4 = musictools.Note.from_frequency(440)
        A3 = musictools.Note.from_frequency(220)
        A5 = musictools.Note.from_frequency(880)
        C4 = musictools.Note.from_frequency(261.6)
        B3 = musictools.Note.from_frequency(246.9)
        B4 = musictools.Note.from_frequency(493.9)
        Db4 = musictools.Note.from_frequency(277.2,"b")
        self.assertEqual(A4.name,"A")
        self.assertEqual(A3.name,"A")
        self.assertEqual(A5.name,"A")
        self.assertEqual(C4.name,"C")
        self.assertEqual(B3.name,"B")
        self.assertEqual(B4.name,"B")
        self.assertEqual(Db4.name,"Db")
        self.assertEqual(A4.octave,4)
        self.assertEqual(A3.octave,3)
        self.assertEqual(A5.octave,5)
        self.assertEqual(C4.octave,4)
        self.assertEqual(B3.octave,3)
        self.assertEqual(B4.octave,4)
        self.assertEqual(Db4.octave,4)
    
    def test_repr(self):
        self.assertEqual(repr(musictools.Note("A#",4,)),'<Note A#4>')
        self.assertEqual(repr(musictools.Note("Gbb",3,"4")),'<Note Gbb3:4>')
        self.assertEqual(repr(musictools.Note("F#",0,"3.t")),'<Note F#0:3.t>')
        self.assertEqual(repr(musictools.Note("B#",3,"5.")),'<Note B#3:5.>')

class TestIntervalClass(unittest.TestCase):

    def test_init(self):

        maj2 = musictools.Interval("M2")
        P12 = musictools.Interval("P5",1)
        min9 = musictools.Interval("m2",1)
        maj72oct = musictools.Interval("M7",2)
        per4 = musictools.Interval("p4")
        aug4 = musictools.Interval("a4")
        dim4 = musictools.Interval("d4")
        doubleaug4 = musictools.Interval("a.4")
        doubledim5 = musictools.Interval("d.4")
        tripletaug2 = musictools.Interval("a..4")
        quadaug2 = musictools.Interval("a...4")
    
    def test_flag_error(self):
        with self.assertRaises(ValueError):
            musictools.Interval("T2")
        with self.assertRaises(ValueError):
            musictools.Interval("M.2")
        with self.assertRaises(ValueError):
            musictools.Interval("m")
        with self.assertRaises(ValueError):
            musictools.Interval("p.4")
        with self.assertRaises(ValueError):
            musictools.Interval("p2")
        with self.assertRaises(ValueError):
            musictools.Interval("M5")

    def test_intvl_diff(self):
        self.assertEqual(musictools.Interval("p1").diff,0)
        self.assertEqual(musictools.Interval("m2").diff,1)
        self.assertEqual(musictools.Interval("M2").diff,2)
        self.assertEqual(musictools.Interval("m3").diff,3)
        self.assertEqual(musictools.Interval("M3").diff,4)
        self.assertEqual(musictools.Interval("P4").diff,5)
        self.assertEqual(musictools.Interval("A4").diff,6)
        self.assertEqual(musictools.Interval("D5").diff,6)
        self.assertEqual(musictools.Interval("p5").diff,7)
        self.assertEqual(musictools.Interval("m6").diff,8)
        self.assertEqual(musictools.Interval("M6").diff,9)
        self.assertEqual(musictools.Interval("D7").diff,9)
        self.assertEqual(musictools.Interval("m7").diff,10)
        self.assertEqual(musictools.Interval("M7").diff,11)
        self.assertEqual(musictools.Interval("a1",1).diff,13)
        self.assertEqual(musictools.Interval("p1",1).diff,12)
        self.assertEqual(musictools.Interval("p1",2).diff,24)
        self.assertEqual(musictools.Interval("M7",1).diff,23)

    def test_letter_diff(self):
        self.assertEqual(musictools.Interval("p1").letter_diff,0)
        self.assertEqual(musictools.Interval("m2").letter_diff,1)
        self.assertEqual(musictools.Interval("M2").letter_diff,1)
        self.assertEqual(musictools.Interval("m3").letter_diff,2)
        self.assertEqual(musictools.Interval("M3").letter_diff,2)
        self.assertEqual(musictools.Interval("P4").letter_diff,3)
        self.assertEqual(musictools.Interval("A4").letter_diff,3)
        self.assertEqual(musictools.Interval("D5").letter_diff,4)
        self.assertEqual(musictools.Interval("p5").letter_diff,4)
        self.assertEqual(musictools.Interval("m6").letter_diff,5)
        self.assertEqual(musictools.Interval("M6").letter_diff,5)
        self.assertEqual(musictools.Interval("D7").letter_diff,6)
        self.assertEqual(musictools.Interval("m7").letter_diff,6)
        self.assertEqual(musictools.Interval("M7").letter_diff,6)
        self.assertEqual(musictools.Interval("a1",1).letter_diff,0)
        self.assertEqual(musictools.Interval("p1",1).letter_diff,0)
        self.assertEqual(musictools.Interval("p1",2).letter_diff,0)
        self.assertEqual(musictools.Interval("M7",1).letter_diff,6)

    def test_intvl_name(self):
        intvl1 = musictools.Interval("p1")
        intvl2 = musictools.Interval("a1")
        intvl3 = musictools.Interval("m2")
        intvl4 = musictools.Interval("M2")
        intvl5 = musictools.Interval("M3")
        intvl6 = musictools.Interval("P4")
        intvl7 = musictools.Interval("D5")
        intvl8 = musictools.Interval("D5",1)
        intvl9 = musictools.Interval("p1",2)
        intvl10 = musictools.Interval("A5")
        intvl11 = musictools.Interval("M7")
        intvl12 = musictools.Interval("d7")
        intvl13 = musictools.Interval("a3")
        intvl14 = musictools.Interval("a..4")
        intvl15 = musictools.Interval("d...5",2)
        intvl16 = musictools.Interval("d.2")
        intvl17 = musictools.Interval("m3",1)
        intvl18 = musictools.Interval("m3",2)
        intvl19 = musictools.Interval("M7",1)
        intvl20 = musictools.Interval("M7",3)
        intvl21 = musictools.Interval("p1",1)
        
        self.assertEqual(intvl1.name,"Perfect unison")
        self.assertEqual(intvl2.name,"Augmented unison")
        self.assertEqual(intvl3.name,"Minor 2nd")
        self.assertEqual(intvl4.name,"Major 2nd")
        self.assertEqual(intvl5.name,"Major 3rd")
        self.assertEqual(intvl6.name,"Perfect 4th")
        self.assertEqual(intvl7.name,"Diminished 5th")
        self.assertEqual(intvl8.name,"Diminished 12th")
        self.assertEqual(intvl9.name,"2 octaves")
        self.assertEqual(intvl10.name,"Augmented 5th")
        self.assertEqual(intvl11.name,"Major 7th")
        self.assertEqual(intvl12.name,"Diminished 7th")
        self.assertEqual(intvl13.name,"Augmented 3rd")
        self.assertEqual(intvl14.name,"Augmented(x3) 4th")
        self.assertEqual(intvl15.name,"Diminished(x4) 5th plus 2 octaves")
        self.assertEqual(intvl16.name,"Diminished(x2) 2nd")
        self.assertEqual(intvl17.name,"Minor 10th")
        self.assertEqual(intvl18.name,"Minor 3rd plus 2 octaves")
        self.assertEqual(intvl19.name,"Major 14th")
        self.assertEqual(intvl20.name,"Major 7th plus 3 octaves")
        self.assertEqual(intvl21.name,"Perfect octave")

    def test_intvl_from_notes(self):
        A = musictools.Note("A")
        B = musictools.Note("B")
        Bb = musictools.Note("Bb")
        As = musictools.Note("A#")
        G = musictools.Note("G")
        Gb = musictools.Note("Gb")
        E = musictools.Note("E")
        Dbb = musictools.Note("Dbb")
        Dss = musictools.Note("D##")

        self.assertEqual(musictools.Interval.from_notes(A,B).name,"Major 2nd")
        self.assertEqual(musictools.Interval.from_notes(A,Bb).name,"Minor 2nd")
        self.assertEqual(musictools.Interval.from_notes(A,As).name,"Augmented unison")
        self.assertEqual(musictools.Interval.from_notes(G,A).name,"Major 2nd")
        self.assertEqual(musictools.Interval.from_notes(Gb,B).name,"Augmented 3rd")
        self.assertEqual(musictools.Interval.from_notes(Dss,Dbb).name,"Diminished(x4) unison")
        self.assertEqual(musictools.Interval.from_notes(E,B).name,"Perfect 5th")
        self.assertEqual(musictools.Interval.from_notes(B,E).name,"Perfect 4th")

        A4 = A
        A4.octave = 4
        A5 = musictools.Note("A",5)
        A6 = musictools.Note("A",6)
        B3 = B
        B3.octave = 3
        G2 = G
        G2.octave = 2
        Bb4 = Bb
        Bb4.octave = 4
        E5 = E
        E5.octave = 5
        Gb2 = Gb
        Gb2.octave = 2
        

        self.assertEqual(musictools.Interval.from_notes(A4,Bb4).name,"Minor 2nd")
        self.assertEqual(musictools.Interval.from_notes(A4,E5).name,"Perfect 5th")
        self.assertEqual(musictools.Interval.from_notes(G2,B3).name,"Major 10th")
        self.assertEqual(musictools.Interval.from_notes(E5,Bb4).name,"Augmented 4th")
        self.assertEqual(musictools.Interval.from_notes(Bb4,E5).name,"Augmented 4th")
        self.assertEqual(musictools.Interval.from_notes(Bb4,E5).name,"Augmented 4th")
        self.assertEqual(musictools.Interval.from_notes(Bb4,E5).name,"Augmented 4th")
        self.assertEqual(musictools.Interval.from_notes(A4,A5).name,"Perfect octave")
        self.assertEqual(musictools.Interval.from_notes(A4,A6).name,"2 octaves")

    def test_note_method(self):
        A5 = musictools.Note("A",5)
        B2 = musictools.Note("B",2)
        Bb3 = musictools.Note("Bb",3)
        As4 = musictools.Note("A#",4)
        G5 = musictools.Note("G",5)
        Gb2 = musictools.Note("Gb",2)
        E6 = musictools.Note("E",6)
        Dbb2 = musictools.Note("Dbb",2)
        Dss3 = musictools.Note("D##",3)

        intvl1 = musictools.Interval("p1")
        intvl2 = musictools.Interval("a1")
        intvl3 = musictools.Interval("m2")
        intvl4 = musictools.Interval("M2")
        intvl5 = musictools.Interval("M3")
        intvl6 = musictools.Interval("P4")
        intvl7 = musictools.Interval("D5")
        intvl8 = musictools.Interval("D5",1)
        intvl9 = musictools.Interval("p1",2)
        intvl10 = musictools.Interval("A5")
        intvl11 = musictools.Interval("M7")
        intvl12 = musictools.Interval("d7")
        intvl13 = musictools.Interval("a3")
        intvl14 = musictools.Interval("a..4")
        intvl15 = musictools.Interval("d...5",2)
        intvl16 = musictools.Interval("d.2")
        intvl17 = musictools.Interval("m3",1)
        intvl18 = musictools.Interval("m3",2)
        intvl19 = musictools.Interval("M7",1)
        intvl20 = musictools.Interval("M7",3)
        intvl21 = musictools.Interval("p1",1)

        self.assertEqual((A5 + intvl1).name, "A")
        self.assertEqual((A5 + intvl2).name, "A#")
        self.assertEqual((B2 + intvl19).name, "A#")
        self.assertEqual((B2 + intvl19).octave, 4)
        self.assertEqual((E6 + intvl15).name, "Bbbbb")
        self.assertEqual((Dss3 + intvl16).name, "Eb")
        self.assertEqual((G5 + intvl20).name, "F#")
        self.assertEqual((G5 + intvl20).octave, 9)

        self.assertEqual((A5 - intvl1).name, "A")
        self.assertEqual((A5 - intvl2).name, "Ab")
        self.assertEqual((B2 - intvl19).name, "C")
        self.assertEqual((B2 - intvl19).octave, 1)
        self.assertEqual((E6 - intvl15).name, "A####")
        self.assertEqual((Dss3 - intvl16).name, "C#####")
        self.assertEqual((G5 - intvl20).name, "Ab")
        self.assertEqual((G5 - intvl20).octave, 1)

class TestModeClass(unittest.TestCase):

    def test_mode_init(self):

        musictools.Mode("A","major")
        musictools.Mode("B","minor")
        musictools.Mode("C","major pentatonic")
        musictools.Mode("D##","melodic minor")
        musictools.Mode("Gb","locrian")
    
    def test_mode_spelling(self):

        Gmm = musictools.Mode("G","melodic minor")
        self.assertEqual(Gmm.spelling[0].name,"G")
        self.assertEqual(Gmm.spelling[1].name,"A")
        self.assertEqual(Gmm.spelling[2].name,"Bb")
        self.assertEqual(Gmm.spelling[3].name,"C")
        self.assertEqual(Gmm.spelling[4].name,"D")
        self.assertEqual(Gmm.spelling[5].name,"E")
        self.assertEqual(Gmm.spelling[6].name,"F#")

        Dsmin = musictools.Mode("D#","minor")
        self.assertEqual(Dsmin.spelling[0].name,"D#")
        self.assertEqual(Dsmin.spelling[1].name,"E#")
        self.assertEqual(Dsmin.spelling[2].name,"F#")
        self.assertEqual(Dsmin.spelling[3].name,"G#")
        self.assertEqual(Dsmin.spelling[4].name,"A#")
        self.assertEqual(Dsmin.spelling[5].name,"B")
        self.assertEqual(Dsmin.spelling[6].name,"C#")

        Eloc = musictools.Mode("E","locrian")
        self.assertEqual(Eloc.spelling[0].name,"E")
        self.assertEqual(Eloc.spelling[1].name,"F")
        self.assertEqual(Eloc.spelling[2].name,"G")
        self.assertEqual(Eloc.spelling[3].name,"A")
        self.assertEqual(Eloc.spelling[4].name,"Bb")
        self.assertEqual(Eloc.spelling[5].name,"C")
        self.assertEqual(Eloc.spelling[6].name,"D")
    
        Fbblues = musictools.Mode("Fb","blues")
        self.assertEqual(Fbblues.spelling[0].name,"Fb")
        self.assertEqual(Fbblues.spelling[1].name,"Abb")
        self.assertEqual(Fbblues.spelling[2].name,"Bbb")
        self.assertEqual(Fbblues.spelling[3].name,"Bb")
        self.assertEqual(Fbblues.spelling[4].name,"Cb")
        self.assertEqual(Fbblues.spelling[5].name,"Ebb")

class TestChordClass(unittest.TestCase):

    def test_chord_init(self):
        musictools.Chord("A")
        musictools.Chord("Gbm7")
        musictools.Chord("Gminor")
        musictools.Chord("B min")
        musictools.Chord("C minor")
        musictools.Chord("G7")
        musictools.Chord("Bmaj9")
        musictools.Chord("Gb13")
        musictools.Chord("Fmin(maj7)")
        musictools.Chord("Db6/9")
        musictools.Chord("Db(6/9)")
        musictools.Chord("F#b13(b9)")
        musictools.Chord("A+")

    def test_chord_intvls(self):
        chord1 = musictools.Chord("A")
        chord2 = musictools.Chord("Gbm7")
        chord3 = musictools.Chord("Gminor")
        chord4 = musictools.Chord("B min")
        chord5 = musictools.Chord("C minor")
        chord6 = musictools.Chord("G7")
        chord7 = musictools.Chord("Bmaj9")
        chord8 = musictools.Chord("Gb13")
        chord9 = musictools.Chord("Fmin(maj7)")
        chord10 = musictools.Chord("Db6/9")
        chord11 = musictools.Chord("Db(6/9)")
        chord12 = musictools.Chord("F#7b13(b9)")
        chord13 = musictools.Chord("A+")
        chord14 = musictools.Chord("F11")
        chord15 = musictools.Chord("E5")
        self.assertIn("M3",chord1.intervals)
        self.assertIn("m7",chord2.intervals)
        self.assertIn("m3",chord3.intervals)
        self.assertIn("P5",chord4.intervals)
        self.assertNotIn("M3",chord5.intervals)
        self.assertIn("m7",chord6.intervals)
        self.assertIn("M7",chord7.intervals)
        self.assertIn("M2",chord8.intervals)
        self.assertNotIn("m7",chord9.intervals)
        self.assertIn("M7",chord9.intervals)
        self.assertIn("M6",chord10.intervals)
        self.assertIn("M6",chord11.intervals)
        self.assertNotIn("m7",chord11.intervals)
        self.assertIn("m2",chord12.intervals)
        self.assertNotIn("M2",chord12.intervals)
        self.assertIn("A5",chord13.intervals)
        self.assertNotIn("M3",chord14.intervals) 
        self.assertNotIn("M3",chord15.intervals) 


if __name__ == "__main__":

    unittest.main()