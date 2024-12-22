import unittest

from assembler import translate_operation
from logger import Logger


class TestLogger(Logger):
    def log(self, value: int, result: str):
        pass

    def log_full(self, val_a: int, val_b: int, result: str):
        pass


class MyTestCase(unittest.TestCase):
    __logger = TestLogger('text.xml')
    
    def test_1(self):
        with self.assertRaises(ValueError):
            translate_operation('sdasd', self.__logger)

    def test_2(self):
        with self.assertRaises(ValueError):
            translate_operation('ASD', self.__logger)

    def test_3(self):
        with self.assertRaises(ValueError):
            translate_operation('LOAD', self.__logger)

    def test_4(self):
        with self.assertRaises(ValueError):
            translate_operation('LOAD 11111111111111111111111111111', self.__logger)

    def test_5(self):
        logger = TestLogger('text.xml')
        result = translate_operation('READ', self.__logger)
        self.assertEqual(result, '0x0c')

    def test_6(self):
        result = translate_operation('LOAD 105', self.__logger)
        self.assertEqual(result, '0x22,0x0d,0x00,0x00')


if __name__ == '__main__':
    unittest.main()
