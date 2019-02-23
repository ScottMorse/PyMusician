import unittest
from pymusician import Mode, Note
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



    def test_append_measure(self):
        staff = Staff(starting_measures=10)
        staff.measures[9].append_note(Note("A",0,"3"))

        self.assertEqual(staff.measures[9].notes[0].name,"A")

        staff.append_measure()
        
        self.assertEqual(staff.measures[9].notes[0].name,"A")
        self.assertEqual(len(staff.measures),11)
        self.assertFalse(staff.measures[9].is_empty)


    def test_insert_measure(self):
        staff = Staff(starting_measures=2)
        staff.measures[0].append_note(Note('A',4,"3"))
        staff.insert_measure_before(0)

        self.assertEqual(len(staff.measures),3)
        self.assertTrue(staff.measures[0].is_empty)
        self.assertEqual(staff.measures[1].notes[0].name,"A") 

    def test_delete_measure(self):
        staff = Staff(starting_measures=10)
        staff.append_note(Note("A",0,"1"))

        self.assertEqual(staff.measures[0].notes[0].name,'A')
        self.assertTrue(staff.measures[0].is_full)

        staff.delete_measure_at(0)
        
        self.assertTrue(staff.measures[0].is_empty)

        staff.delete_measure_at(2)

        self.assertEqual(len(staff.measures),8)

        with self.assertRaises(Exception):
            staff.delete_measure_at(8)

    def test_appending_error(self):
        staff = Staff(starting_measures=1)

        staff.append_note(Note("A",4,"1"))
        staff.append_note(Note("A",5,"1"))
      
        self.assertEqual(staff.measures[0].notes[0].octave,4)
        self.assertTrue(staff.measures[0].is_full)

        self.assertEqual(staff.measures[1].notes[0].octave,5)

        with self.assertRaises(Exception):
            staff.append_note(Note("A",4,"1."))

        staff34 = Staff(time_sig=TimeSignature(3,4))

        staff34.append_note(Note("A",4,"2."))
        staff34.append_note(Note("A",4,"2"))
        staff34.append_note(Note("A",4,"3"))
        staff34.append_note(Note("A",4,"4"))

        self.assertEqual(len(staff34.measures),3)
        self.assertTrue(staff34.measures[0].is_full)
        self.assertTrue(staff34.measures[1].is_full)
        self.assertFalse(staff34.measures[2].is_empty)
        self.assertFalse(staff34.measures[2].is_full)

        with self.assertRaises(Exception):
            staff34.append_note(Note("A",4,"1"))

    def test_clear_measures(self):
        staff34 = Staff(time_sig=TimeSignature(3,4))

        staff34.append_note(Note("A",4,"2."))
        staff34.append_note(Note("A",4,"2"))
        staff34.append_note(Note("A",4,"3"))
        staff34.append_note(Note("A",4,"4"))

        staff34.clear_selected_measures(0,2)

        self.assertTrue(staff34.measures[0].is_empty)
        self.assertTrue(staff34.measures[1].is_empty)

    def test_delete_measures(self):
        staff = Staff(starting_measures=4)

        staff.measures[len(staff.measures) - 1].append_note(Note('A',4,'1'))

        staff.delete_measure_at(0)

        self.assertEqual(len(staff.measures),3)
        self.assertEqual(staff.measures[len(staff.measures) - 1].notes[0].name,'A')

        staff.delete_selected_measures(0,2)

        self.assertEqual(len(staff.measures),1)
        self.assertEqual(len(staff.measures[0].notes),1)

if __name__ == "__main__":

    unittest.main()