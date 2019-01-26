import unittest
import pymusician as pm

class TestModeClass(unittest.TestCase):

    def test_mode_init(self):

        pm.Mode("A","major")
        pm.Mode("B","minor")
        pm.Mode("C","major pentatonic")
        pm.Mode("D##","melodic minor")
        pm.Mode("Gb","locrian")
    
    def test_mode_spelling(self):

        Amaj = pm.Mode("A","major")
        self.assertEqual(Amaj.name,"A major")
        self.assertEqual(Amaj.spelling[0].name,"A")
        self.assertEqual(Amaj.spelling[1].name,"B")
        self.assertEqual(Amaj.spelling[2].name,"C#")
        self.assertEqual(Amaj.spelling[3].name,"D")
        self.assertEqual(Amaj.spelling[4].name,"E")
        self.assertEqual(Amaj.spelling[5].name,"F#")
        self.assertEqual(Amaj.spelling[6].name,"G#")

        Gmm = pm.Mode("G","melodic minor")
        self.assertEqual(Gmm.spelling[0].name,"G")
        self.assertEqual(Gmm.spelling[1].name,"A")
        self.assertEqual(Gmm.spelling[2].name,"Bb")
        self.assertEqual(Gmm.spelling[3].name,"C")
        self.assertEqual(Gmm.spelling[4].name,"D")
        self.assertEqual(Gmm.spelling[5].name,"E")
        self.assertEqual(Gmm.spelling[6].name,"F#")

        Ehm = pm.Mode("E","harmonic minor")
        self.assertEqual(Ehm.spelling[0].name,"E")
        self.assertEqual(Ehm.spelling[1].name,"F#")
        self.assertEqual(Ehm.spelling[2].name,"G")
        self.assertEqual(Ehm.spelling[3].name,"A")
        self.assertEqual(Ehm.spelling[4].name,"B")
        self.assertEqual(Ehm.spelling[5].name,"C")
        self.assertEqual(Ehm.spelling[6].name,"D#")

        Espent = pm.Mode("E#","major pentatonic")
        self.assertEqual(Espent.spelling[0].name,"E#")
        self.assertEqual(Espent.spelling[1].name,"F##")
        self.assertEqual(Espent.spelling[2].name,"G##")
        self.assertEqual(Espent.spelling[3].name,"B#")
        self.assertEqual(Espent.spelling[4].name,"C##")

        Blydom = pm.Mode("B","lydian dominant")
        self.assertEqual(Blydom.spelling[0].name,"B")
        self.assertEqual(Blydom.spelling[1].name,"C#")
        self.assertEqual(Blydom.spelling[2].name,"D#")
        self.assertEqual(Blydom.spelling[3].name,"E#")
        self.assertEqual(Blydom.spelling[4].name,"F#")
        self.assertEqual(Blydom.spelling[5].name,"G#")
        self.assertEqual(Blydom.spelling[6].name,"A")
        
        Caug = pm.Mode("C","augmented")
        self.assertEqual(Caug.spelling[0].name,"C")
        self.assertEqual(Caug.spelling[1].name,"D#")
        self.assertEqual(Caug.spelling[2].name,"E")
        self.assertEqual(Caug.spelling[3].name,"G")
        self.assertEqual(Caug.spelling[4].name,"G#")
        self.assertEqual(Caug.spelling[5].name,"B")

        Dsmin = pm.Mode("D#","minor")
        self.assertEqual(Dsmin.spelling[0].name,"D#")
        self.assertEqual(Dsmin.spelling[1].name,"E#")
        self.assertEqual(Dsmin.spelling[2].name,"F#")
        self.assertEqual(Dsmin.spelling[3].name,"G#")
        self.assertEqual(Dsmin.spelling[4].name,"A#")
        self.assertEqual(Dsmin.spelling[5].name,"B")
        self.assertEqual(Dsmin.spelling[6].name,"C#")

        Eloc = pm.Mode("E","locrian")
        self.assertEqual(Eloc.spelling[0].name,"E")
        self.assertEqual(Eloc.spelling[1].name,"F")
        self.assertEqual(Eloc.spelling[2].name,"G")
        self.assertEqual(Eloc.spelling[3].name,"A")
        self.assertEqual(Eloc.spelling[4].name,"Bb")
        self.assertEqual(Eloc.spelling[5].name,"C")
        self.assertEqual(Eloc.spelling[6].name,"D")
    
        Fbblues = pm.Mode("Fb","blues")
        self.assertEqual(Fbblues.spelling[0].name,"Fb")
        self.assertEqual(Fbblues.spelling[1].name,"Abb")
        self.assertEqual(Fbblues.spelling[2].name,"Bbb")
        self.assertEqual(Fbblues.spelling[3].name,"Bb")
        self.assertEqual(Fbblues.spelling[4].name,"Cb")
        self.assertEqual(Fbblues.spelling[5].name,"Ebb")
    
if __name__ == "__main__":

    unittest.main()