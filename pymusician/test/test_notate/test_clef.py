import unittest
from pymusician import notate

class TestClefClass(unittest.TestCase):

    def test_initialization(self):

        notate.Clef("treble")
        notate.Clef("soprano")
        notate.Clef("suboctave treble")

        with self.assertRaises(ValueError):
            notate.Clef("trebly")
        with self.assertRaises(ValueError):
            notate.Clef(1)
    
    def test_C4_position(self):

        treble = notate.Clef("treble")
        subtreble = notate.Clef("suboctave treble")
        bass = notate.Clef("bass")
        soprano = notate.Clef("soprano")
        mezzosoprano = notate.Clef("mezzo-soprano")
        alto = notate.Clef("alto")
        tenor = notate.Clef("tenor")
        baritone = notate.Clef("baritone")
        frenchviolin = notate.Clef("french violin")
        neutral = notate.Clef("neutral")

        self.assertEqual(treble.C4_position,-1)
        self.assertEqual(treble.clef_type,"G")
        self.assertEqual(subtreble.C4_position,-1)
        self.assertEqual(subtreble.clef_type,"G8vb")
        self.assertEqual(bass.C4_position,10)
        self.assertEqual(bass.clef_type,"F")
        self.assertEqual(soprano.C4_position,1)
        self.assertEqual(soprano.clef_type,"C")
        self.assertEqual(mezzosoprano.C4_position,3)
        self.assertEqual(mezzosoprano.clef_type,"C")
        self.assertEqual(alto.C4_position,5)
        self.assertEqual(alto.clef_type,"C")
        self.assertEqual(tenor.C4_position,7)
        self.assertEqual(tenor.clef_type,"C")
        self.assertEqual(baritone.C4_position,9)
        self.assertEqual(baritone.clef_type,"C")
        self.assertEqual(frenchviolin.C4_position,-3)
        self.assertEqual(frenchviolin.clef_type,"G")
        self.assertEqual(neutral.C4_position,None)
        self.assertEqual(neutral.clef_type,"Neutral")

    def test_custom_clefs(self):

        custom1 = notate.Clef("poopoo",0,"G")
        
        self.assertEqual(custom1.clef_name,"poopoo")
        self.assertEqual(custom1.C4_position,0)
        self.assertEqual(custom1.clef_type,"G")

        with self.assertRaises(ValueError):
            notate.Clef(12,2,"C")
        with self.assertRaises(ValueError):
            notate.Clef("hoookay","2","C")
        with self.assertRaises(ValueError):
            notate.Clef("okey dokey",2,4)

if __name__ == "__main__":

    unittest.main()