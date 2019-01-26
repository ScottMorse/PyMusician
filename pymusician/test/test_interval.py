import unittest
import pymusician as pm

class TestIntervalClass(unittest.TestCase):

    def test_init(self):

        maj2 = pm.Interval("M2")
        P12 = pm.Interval("P5",1)
        min9 = pm.Interval("m2",1)
        maj72oct = pm.Interval("M7",2)
        per4 = pm.Interval("p4")
        aug4 = pm.Interval("a4")
        dim4 = pm.Interval("d4")
        doubleaug4 = pm.Interval("a.4")
        doubledim5 = pm.Interval("d.4")
        tripletaug2 = pm.Interval("a..4")
        quadaug2 = pm.Interval("a...4")
    
    def test_flag_error(self):
        with self.assertRaises(ValueError):
            pm.Interval("T2")
        with self.assertRaises(ValueError):
            pm.Interval("M.2")
        with self.assertRaises(ValueError):
            pm.Interval("m")
        with self.assertRaises(ValueError):
            pm.Interval("p.4")
        with self.assertRaises(ValueError):
            pm.Interval("p2")
        with self.assertRaises(ValueError):
            pm.Interval("M5")

    def test_intvl_diff(self):
        self.assertEqual(pm.Interval("p1").diff,0)
        self.assertEqual(pm.Interval("m2").diff,1)
        self.assertEqual(pm.Interval("M2").diff,2)
        self.assertEqual(pm.Interval("m3").diff,3)
        self.assertEqual(pm.Interval("M3").diff,4)
        self.assertEqual(pm.Interval("P4").diff,5)
        self.assertEqual(pm.Interval("A4").diff,6)
        self.assertEqual(pm.Interval("D5").diff,6)
        self.assertEqual(pm.Interval("p5").diff,7)
        self.assertEqual(pm.Interval("m6").diff,8)
        self.assertEqual(pm.Interval("M6").diff,9)
        self.assertEqual(pm.Interval("D7").diff,9)
        self.assertEqual(pm.Interval("m7").diff,10)
        self.assertEqual(pm.Interval("M7").diff,11)
        self.assertEqual(pm.Interval("a1",1).diff,13)
        self.assertEqual(pm.Interval("p1",1).diff,12)
        self.assertEqual(pm.Interval("p1",2).diff,24)
        self.assertEqual(pm.Interval("M7",1).diff,23)

    def test_letter_diff(self):
        self.assertEqual(pm.Interval("p1").letter_diff,0)
        self.assertEqual(pm.Interval("m2").letter_diff,1)
        self.assertEqual(pm.Interval("M2").letter_diff,1)
        self.assertEqual(pm.Interval("m3").letter_diff,2)
        self.assertEqual(pm.Interval("M3").letter_diff,2)
        self.assertEqual(pm.Interval("P4").letter_diff,3)
        self.assertEqual(pm.Interval("A4").letter_diff,3)
        self.assertEqual(pm.Interval("D5").letter_diff,4)
        self.assertEqual(pm.Interval("p5").letter_diff,4)
        self.assertEqual(pm.Interval("m6").letter_diff,5)
        self.assertEqual(pm.Interval("M6").letter_diff,5)
        self.assertEqual(pm.Interval("D7").letter_diff,6)
        self.assertEqual(pm.Interval("m7").letter_diff,6)
        self.assertEqual(pm.Interval("M7").letter_diff,6)
        self.assertEqual(pm.Interval("a1",1).letter_diff,0)
        self.assertEqual(pm.Interval("p1",1).letter_diff,0)
        self.assertEqual(pm.Interval("p1",2).letter_diff,0)
        self.assertEqual(pm.Interval("M7",1).letter_diff,6)

    def test_intvl_name(self):
        intvl1 = pm.Interval("p1")
        intvl2 = pm.Interval("a1")
        intvl3 = pm.Interval("m2")
        intvl4 = pm.Interval("M2")
        intvl5 = pm.Interval("M3")
        intvl6 = pm.Interval("P4")
        intvl7 = pm.Interval("D5")
        intvl8 = pm.Interval("D5",1)
        intvl9 = pm.Interval("p1",2)
        intvl10 = pm.Interval("A5")
        intvl11 = pm.Interval("M7")
        intvl12 = pm.Interval("d7")
        intvl13 = pm.Interval("a3")
        intvl14 = pm.Interval("a..4")
        intvl15 = pm.Interval("d...5",2)
        intvl16 = pm.Interval("d.2")
        intvl17 = pm.Interval("m3",1)
        intvl18 = pm.Interval("m3",2)
        intvl19 = pm.Interval("M7",1)
        intvl20 = pm.Interval("M7",3)
        intvl21 = pm.Interval("p1",1)
        
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
        A = pm.Note("A")
        B = pm.Note("B")
        Bb = pm.Note("Bb")
        As = pm.Note("A#")
        G = pm.Note("G")
        Gb = pm.Note("Gb")
        E = pm.Note("E")
        Dbb = pm.Note("Dbb")
        Dss = pm.Note("D##")

        self.assertEqual(pm.Interval.from_notes(A,B).name,"Major 2nd")
        self.assertEqual(pm.Interval.from_notes(A,Bb).name,"Minor 2nd")
        self.assertEqual(pm.Interval.from_notes(A,As).name,"Augmented unison")
        self.assertEqual(pm.Interval.from_notes(G,A).name,"Major 2nd")
        self.assertEqual(pm.Interval.from_notes(Gb,B).name,"Augmented 3rd")
        self.assertEqual(pm.Interval.from_notes(Dss,Dbb).name,"Diminished(x4) unison")
        self.assertEqual(pm.Interval.from_notes(E,B).name,"Perfect 5th")
        self.assertEqual(pm.Interval.from_notes(B,E).name,"Perfect 4th")

        A4 = A
        A4.octave = 4
        A5 = pm.Note("A",5)
        A6 = pm.Note("A",6)
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
        

        self.assertEqual(pm.Interval.from_notes(A4,Bb4).name,"Minor 2nd")
        self.assertEqual(pm.Interval.from_notes(A4,E5).name,"Perfect 5th")
        self.assertEqual(pm.Interval.from_notes(G2,B3).name,"Major 10th")
        self.assertEqual(pm.Interval.from_notes(E5,Bb4).name,"Augmented 4th")
        self.assertEqual(pm.Interval.from_notes(Bb4,E5).name,"Augmented 4th")
        self.assertEqual(pm.Interval.from_notes(Bb4,E5).name,"Augmented 4th")
        self.assertEqual(pm.Interval.from_notes(Bb4,E5).name,"Augmented 4th")
        self.assertEqual(pm.Interval.from_notes(A4,A5).name,"Perfect octave")
        self.assertEqual(pm.Interval.from_notes(A4,A6).name,"2 octaves")

    def test_note_method(self):
        A5 = pm.Note("A",5)
        B2 = pm.Note("B",2)
        Bb3 = pm.Note("Bb",3)
        As4 = pm.Note("A#",4)
        G5 = pm.Note("G",5)
        Gb2 = pm.Note("Gb",2)
        E6 = pm.Note("E",6)
        Dbb2 = pm.Note("Dbb",2)
        Dss3 = pm.Note("D##",3)

        intvl1 = pm.Interval("p1")
        intvl2 = pm.Interval("a1")
        intvl3 = pm.Interval("m2")
        intvl4 = pm.Interval("M2")
        intvl5 = pm.Interval("M3")
        intvl6 = pm.Interval("P4")
        intvl7 = pm.Interval("D5")
        intvl8 = pm.Interval("D5",1)
        intvl9 = pm.Interval("p1",2)
        intvl10 = pm.Interval("A5")
        intvl11 = pm.Interval("M7")
        intvl12 = pm.Interval("d7")
        intvl13 = pm.Interval("a3")
        intvl14 = pm.Interval("a..4")
        intvl15 = pm.Interval("d...5",2)
        intvl16 = pm.Interval("d.2")
        intvl17 = pm.Interval("m3",1)
        intvl18 = pm.Interval("m3",2)
        intvl19 = pm.Interval("M7",1)
        intvl20 = pm.Interval("M7",3)
        intvl21 = pm.Interval("p1",1)

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

if __name__ == "__main__":

    unittest.main()