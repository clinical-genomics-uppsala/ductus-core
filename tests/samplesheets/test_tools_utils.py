import unittest
from ductuscore.tools.utils import parse_sample_sheet


class TestUtils(unittest.TestCase):

    def test_parse_haloplex(self):
        result = parse_sample_sheet("tests/samplesheets/files/SampleSheet.haloplex.csv")
        self.assertEqual((('haloplex', True), ('tso500', False), ('te', False), ('tm', False)), result)

    def test_parse_tso500(self):
        result = parse_sample_sheet("tests/samplesheets/files/SampleSheet.tso500.csv")
        self.assertEqual((('haloplex', False), ('tso500', True), ('te', False), ('tm', False)), result)

    def test_parse_tm(self):
        result = parse_sample_sheet("tests/samplesheets/files/SampleSheet.tm.csv")
        self.assertEqual((('haloplex', False), ('tso500', False), ('te', False), ('tm', True)), result)

    def test_parse_te(self):
        result = parse_sample_sheet("tests/samplesheets/files/SampleSheet.te.csv")
        self.assertEqual((('haloplex', False), ('tso500', False), ('te', True), ('tm', False)), result)


if __name__ == '__main__':
    unittest.main()
