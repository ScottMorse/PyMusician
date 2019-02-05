import unittest
import pymusician as pm

class TestModeClass(unittest.TestCase):

    def test_mode_init(self):

        pm.Mode("A","major")
        pm.Mode("B","minor")
        pm.Mode("C","major pentatonic")
        pm.Mode("D##","melodic minor")
        pm.Mode("Gb","locrian")

        with self.assertRaises(ValueError):
            pm.Mode("H","major")
        with self.assertRaises(ValueError):
            pm.Mode("Az","major")
        with self.assertRaises(ValueError):
            pm.Mode("G","stupid")
        with self.assertRaises(ValueError):
            pm.Mode("A","majory")
    
    def test_mode_spelling(self):

        Amaj = pm.Mode("A","major")
        self.assertEqual(Amaj.name,"A major")
        self.assertEqual(Amaj[0].name,"A")
        self.assertEqual(Amaj[1].name,"B")
        self.assertEqual(Amaj[2].name,"C#")
        self.assertEqual(Amaj[3].name,"D")
        self.assertEqual(Amaj[4].name,"E")
        self.assertEqual(Amaj[5].name,"F#")
        self.assertEqual(Amaj[6].name,"G#")

        Gmm = pm.Mode("G","melodic minor")
        self.assertEqual(Gmm[0].name,"G")
        self.assertEqual(Gmm[1].name,"A")
        self.assertEqual(Gmm[2].name,"Bb")
        self.assertEqual(Gmm[3].name,"C")
        self.assertEqual(Gmm[4].name,"D")
        self.assertEqual(Gmm[5].name,"E")
        self.assertEqual(Gmm[6].name,"F#")

        Ehm = pm.Mode("E","harmonic minor")
        self.assertEqual(Ehm[0].name,"E")
        self.assertEqual(Ehm[1].name,"F#")
        self.assertEqual(Ehm[2].name,"G")
        self.assertEqual(Ehm[3].name,"A")
        self.assertEqual(Ehm[4].name,"B")
        self.assertEqual(Ehm[5].name,"C")
        self.assertEqual(Ehm[6].name,"D#")

        Espent = pm.Mode("E#","major pentatonic")
        self.assertEqual(Espent[0].name,"E#")
        self.assertEqual(Espent[1].name,"F##")
        self.assertEqual(Espent[2].name,"G##")
        self.assertEqual(Espent[3].name,"B#")
        self.assertEqual(Espent[4].name,"C##")

        Blydom = pm.Mode("B","lydian dominant")
        self.assertEqual(Blydom[0].name,"B")
        self.assertEqual(Blydom[1].name,"C#")
        self.assertEqual(Blydom[2].name,"D#")
        self.assertEqual(Blydom[3].name,"E#")
        self.assertEqual(Blydom[4].name,"F#")
        self.assertEqual(Blydom[5].name,"G#")
        self.assertEqual(Blydom[6].name,"A")
        
        Caug = pm.Mode("C","augmented")
        self.assertEqual(Caug[0].name,"C")
        self.assertEqual(Caug[1].name,"D#")
        self.assertEqual(Caug[2].name,"E")
        self.assertEqual(Caug[3].name,"G")
        self.assertEqual(Caug[4].name,"G#")
        self.assertEqual(Caug[5].name,"B")

        Dsmin = pm.Mode("D#","minor")
        self.assertEqual(Dsmin[0].name,"D#")
        self.assertEqual(Dsmin[1].name,"E#")
        self.assertEqual(Dsmin[2].name,"F#")
        self.assertEqual(Dsmin[3].name,"G#")
        self.assertEqual(Dsmin[4].name,"A#")
        self.assertEqual(Dsmin[5].name,"B")
        self.assertEqual(Dsmin[6].name,"C#")

        Eloc = pm.Mode("E","locrian")
        self.assertEqual(Eloc[0].name,"E")
        self.assertEqual(Eloc[1].name,"F")
        self.assertEqual(Eloc[2].name,"G")
        self.assertEqual(Eloc[3].name,"A")
        self.assertEqual(Eloc[4].name,"Bb")
        self.assertEqual(Eloc[5].name,"C")
        self.assertEqual(Eloc[6].name,"D")
    
        Fbblues = pm.Mode("Fb","blues")
        self.assertEqual(Fbblues[0].name,"Fb")
        self.assertEqual(Fbblues[1].name,"Abb")
        self.assertEqual(Fbblues[2].name,"Bbb")
        self.assertEqual(Fbblues[3].name,"Bb")
        self.assertEqual(Fbblues[4].name,"Cb")
        self.assertEqual(Fbblues[5].name,"Ebb")
    
    def test_custom_modes(self):

        with self.assertRaises(ValueError):
            pm.Mode("A","something",["Hi",1,2,3,4,5,6])
        with self.assertRaises(ValueError):
            pm.Mode("A","something",[1,1,1,1,1],[1,1,1,1,1,1])
        with self.assertRaises(ValueError):
            pm.Mode("A","something",[1,2,3,4,1],[1,2,2])
        with self.assertRaises(ValueError):
            pm.Mode("A","something",[1,2,3,4,5,6,12])
        with self.assertRaises(ValueError):
            pm.Mode("A","something",[1,2,3,4,5,6,7],[1,2,3,4,5,6,7])

        custom_mode1 = pm.Mode("A","custom",[1,1,1,1])
        custom_mode2 = pm.Mode("A","custom major",[2,2,1,2,2,2,1],[1,1,1,1,1,1,1])
        custom_mode3 = pm.Mode("G","custom harmonic minor",[2,1,2,2,1,3,1],[1,1,1,1,1,1,1])
        custom_mode4 = pm.Mode("Fb","custom",[1,2,2,3,1],[1,1,1,1,1])
        custom_mode5 = pm.Mode("E","custom",[1,2,3,4,5],[2,3,6,1,2])

        self.assertEqual(len(custom_mode1),4)
        self.assertEqual(custom_mode1[0].name,"A")
        self.assertEqual(custom_mode1[1].name,"Bb")
        self.assertEqual(custom_mode1[2].name,"B")
        self.assertEqual(custom_mode1[3].name,"C")

        self.assertEqual(custom_mode2.name,"A custom major")
        self.assertEqual(custom_mode2[0].name,"A")
        self.assertEqual(custom_mode2[1].name,"B")
        self.assertEqual(custom_mode2[2].name,"C#")
        self.assertEqual(custom_mode2[3].name,"D")
        self.assertEqual(custom_mode2[4].name,"E")
        self.assertEqual(custom_mode2[5].name,"F#")
        self.assertEqual(custom_mode2[6].name,"G#")

        self.assertEqual(custom_mode3[0].name,"G")
        self.assertEqual(custom_mode3[1].name,"A")
        self.assertEqual(custom_mode3[2].name,"Bb")
        self.assertEqual(custom_mode3[3].name,"C")
        self.assertEqual(custom_mode3[4].name,"D")
        self.assertEqual(custom_mode3[5].name,"Eb")
        self.assertEqual(custom_mode3[6].name,"F#")

        self.assertEqual(custom_mode4[0].name,"Fb")
        self.assertEqual(custom_mode4[1].name,"Gbb")
        self.assertEqual(custom_mode4[2].name,"Abb")
        self.assertEqual(custom_mode4[3].name,"Bbb")
        self.assertEqual(custom_mode4[4].name,"C")

        self.assertEqual(custom_mode5[0].name,"E")
        self.assertEqual(custom_mode5[1].name,"Gbb")
        self.assertEqual(custom_mode5[2].name,"Cbbbbb")
        self.assertEqual(custom_mode5[3].name,"Bb")
        self.assertEqual(custom_mode5[4].name,"C##")

if __name__ == "__main__":

    unittest.main()