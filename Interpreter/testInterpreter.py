import unittest
from io import UnsupportedOperation

from interpreter import make_operation


class MyTestCase(unittest.TestCase):
    def test_1(self):
        with self.assertRaises(UnsupportedOperation):
            make_operation(['e1'], '', {})

    def test_2(self):
        with self.assertRaises(ValueError):
            make_operation(['e2', 'ff', 'ff', 'ff', 'ff', '7f'], '', {})

    def test_3(self):
        memory = { 'c1': 'e2' }
        mregister = 'c1'
        
        result = make_operation(['0c'], mregister, memory)
        self.assertEqual(result, 'e2')
 

if __name__ == '__main__':
    unittest.main()
