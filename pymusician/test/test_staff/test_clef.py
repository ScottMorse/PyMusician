import unittest
from pymusician import staff

class TestClefClass(unittest.TestCase):

    def test_initialization(self):

        staff.Clef("treble")
        staff.Clef("soprano")
        staff.Clef("suboctave treble")

        with self.assertRaises(ValueError):
            staff.Clef("trebly")
        with self.assertRaises(ValueError):
            staff.Clef(1)
    
    def test_C4_position(self):

        treble = staff.Clef("treble")
        subtreble = staff.Clef("suboctave treble")
        bass = staff.Clef("bass")
        soprano = staff.Clef("soprano")
        mezzosoprano = staff.Clef("mezzo-soprano")
        alto = staff.Clef("alto")
        tenor = staff.Clef("tenor")
        baritone = staff.Clef("baritone")
        frenchviolin = staff.Clef("french violin")
        neutral = staff.Clef("neutral")

        self.assertEqual(treble.C4_position,-1)
        self.assertEqual(subtreble.C4_position,-1)
        self.assertEqual(bass.C4_position,10)
        self.assertEqual(soprano.C4_position,1)
        self.assertEqual(mezzosoprano.C4_position,3)
        self.assertEqual(alto.C4_position,5)
        self.assertEqual(tenor.C4_position,7)
        self.assertEqual(baritone.C4_position,9)
        self.assertEqual(frenchviolin.C4_position,-3)
        self.assertEqual(neutral.C4_position,None)

    def test_custom_clefs(self):

        custom1 = staff.Clef("poopoo",0,"G")
        
        self.assertEqual(custom1.clef_name,"poopoo")
        self.assertEqual(custom1.C4_position,0)
        self.assertEqual(custom1.clef_type,"G")

        with self.assertRaises(ValueError):
            staff.Clef(12,2,"C")
        with self.assertRaises(ValueError):
            staff.Clef("hoookay","2","C")
        with self.assertRaises(ValueError):
            staff.Clef("okey dokey",2,4)

if __name__ == "__main__":

    unittest.main()