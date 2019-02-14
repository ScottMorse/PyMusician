import unittest
from pymusician import Mode
from pymusician.notate import TimeSignature, Staff

class TestStaffClass(unittest.TestCase):

    def test_initialization(self):
        Staff()
        Staff("A",TimeSignature(3,4),starting_measures=0,bpm=120)
        
        with self.assertRaises(ValueError):
            Staff("Az")
        with self.assertRaises(ValueError):
            Staff(time_sig="Blah")
        with self.assertRaises(ValueError):
            Staff(time_sig=TimeSignature(-1,2))
        with self.assertRaises(ValueError):
            Staff(starting_measures=-1)
        
    def test_starting_measures(self):
        staff = Staff(starting_measures=10)

        self.assertEqual(len(staff.measures),10)

        for measure in staff.measures:
            self.assertTrue(measure.is_empty)
            self.assertEqual(measure._measure_len, 128 * 4)
            self.assertFalse(measure.is_full)

        staff2 = Staff("A",TimeSignature(3,8))
        
        self.assertEqual(len(staff2.measures),1)
        self.assertEqual(staff2.measures[0].measure_len,64 * 3)

    

if __name__ == "__main__":

    unittest.main()