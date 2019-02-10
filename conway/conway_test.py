import unittest
from conway import get_next_generation_state

class ConwayTest(unittest.TestCase):
    """Test class"""

    def test_next_generation_case(self):
        """Tests the function that applies base Conway logic"""
        state_1 = get_next_generation_state(True, 0)
        self.assertEqual(state_1, 0)
        state_2 = get_next_generation_state(True, 1)
        self.assertEqual(state_2, 0)
        state_3 = get_next_generation_state(True, 2)
        self.assertEqual(state_3, 1)
        state_4 = get_next_generation_state(True, 3)
        self.assertEqual(state_4, 1)
        for i in range(4, 9):
            self.assertEqual(get_next_generation_state(True, i), 0)
        self.assertEqual(get_next_generation_state(False, 3), 1)
        for i in range(9):
            if i != 3:
                self.assertEqual(get_next_generation_state(False, i), 0)
