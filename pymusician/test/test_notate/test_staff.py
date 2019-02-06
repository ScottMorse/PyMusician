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

if __name__ == "__main__":

    unittest.main()