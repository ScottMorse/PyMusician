import unittest
import pymusician as pm

class TestTimeSignatureClass(unittest.TestCase):

    def test_initialization(self):
        pm.TimeSignature(1,1)
        pm.TimeSignature(3,2)
        pm.TimeSignature(4,4)
        pm.TimeSignature(5,8)
        pm.TimeSignature(6,16)
        pm.TimeSignature(8,32)
        pm.TimeSignature(10,64)
        pm.TimeSignature(12,128)
        pm.TimeSignature(8,256)
        pm.TimeSignature(256,512)

        with self.assertRaises(ValueError):
            pm.TimeSignature("1","3")
        with self.assertRaises(ValueError):
            pm.TimeSignature(1,3.5)
        with self.assertRaises(ValueError):
            pm.TimeSignature(0,4)
        with self.assertRaises(ValueError):
            pm.TimeSignature(-1,4)
        with self.assertRaises(ValueError):
            pm.TimeSignature(3,513)
    
    def test_basic_properties(self):
        timesig = pm.TimeSignature(4,8)
        self.assertEqual(timesig.top_number,4)
        self.assertEqual(timesig.bottom_number,8)

    def test_beat_len(self):
        common = pm.TimeSignature(4,4)
        cut = pm.TimeSignature(2,2)
        six_eight = pm.TimeSignature(6,8)

        self.assertEqual(common.beat_len,128)
        self.assertEqual(cut.beat_len,256)
        self.assertEqual(six_eight.beat_len,64)
    
    def test_gets_beat(self):
        timesig1 = pm.TimeSignature(1,1)
        timesig2 = pm.TimeSignature(3,2)
        timesig3 = pm.TimeSignature(4,4)
        timesig4 = pm.TimeSignature(5,8)
        timesig5 = pm.TimeSignature(6,16)
        timesig6 = pm.TimeSignature(8,32)
        timesig7 = pm.TimeSignature(10,64)
        timesig8 = pm.TimeSignature(12,128)
        timesig9 = pm.TimeSignature(8,256)
        timesig10 = pm.TimeSignature(256,512)

        self.assertEqual(timesig1.gets_beat,"whole")
        self.assertEqual(timesig2.gets_beat,"half")
        self.assertEqual(timesig3.gets_beat,"quarter")
        self.assertEqual(timesig4.gets_beat,"8th")
        self.assertEqual(timesig5.gets_beat,"16th")
        self.assertEqual(timesig6.gets_beat,"32nd")
        self.assertEqual(timesig7.gets_beat,"64th")
        self.assertEqual(timesig8.gets_beat,"128th")
        self.assertEqual(timesig9.gets_beat,"256th")
        self.assertEqual(timesig10.gets_beat,"512th")

    def test_measure_len(self):
        timesig1 = pm.TimeSignature(1,1)
        timesig2 = pm.TimeSignature(3,2)
        timesig3 = pm.TimeSignature(4,4)
        timesig4 = pm.TimeSignature(5,8)
        timesig5 = pm.TimeSignature(6,16)
        timesig6 = pm.TimeSignature(8,32)
        timesig7 = pm.TimeSignature(10,64)
        timesig8 = pm.TimeSignature(12,128)
        timesig9 = pm.TimeSignature(8,256)
        timesig10 = pm.TimeSignature(256,512)

        self.assertEqual(timesig1.measure_len,512)
        self.assertEqual(timesig2.measure_len,768)
        self.assertEqual(timesig3.measure_len,512)
        self.assertEqual(timesig4.measure_len,320)
        self.assertEqual(timesig5.measure_len,192)
        self.assertEqual(timesig6.measure_len,128)
        self.assertEqual(timesig7.measure_len,80)
        self.assertEqual(timesig8.measure_len,48)
        self.assertEqual(timesig9.measure_len,16)
        self.assertEqual(timesig10.measure_len,256)
    
if __name__ == "__main__":

    unittest.main()