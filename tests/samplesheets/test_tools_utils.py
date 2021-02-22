import unittest
from ductus.tools.utils import extract_analysis_information, contains


class TestUtils(unittest.TestCase):

    def test_parse_haloplex(self):
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.haloplex.csv")

        self.assertEqual("[Header]\n"
                         "Local Run Manager Analysis Id,56056\n"
                         "Experiment Name,20210203_LU\n"
                         "Date,2021-02-04\n"
                         "Module,GenerateFASTQ - 2.0.0\n"
                         "Workflow,GenerateFASTQ\n"
                         "Library Prep Kit,HaloPlex\n"
                         "Chemistry,Default\n"
                         "\n"
                         "[Reads]\n"
                         "151\n"
                         "151\n"
                         "\n"
                         "[Data]\n"
                         "Sample_ID,Sample_Name,Description,index,I7_Index_ID,Sample_Project\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [('97-181', 'sera', '97-181,97-181,,ACCTCCAA,E03,\n'),
                         ('97-217', 'sera', '97-217,97-217,,GCGAGTAA,F03,\n'),
                         ('97-218', 'sera', '97-218,97-218,,ACTATGCA,G03,\n'),
                         ('97-219', 'sera', '97-219,97-219,,CGGATTGC,H03,\n'),
                         ('97-220', 'sera', '97-220,97-220,,AACTCACC,A04,\n'),
                         ('97-221', 'sera', '97-221,97-221,,GCTAACGA,B04,\n')])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

    def test_parse_tso500(self):
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.tso500.csv")
        self.assertEqual("[Header],,,,,,,,,,,\n"
                         "IEMFileVersion,4,,,,,,,,,,\n"
                         "Investigator Name,,,,,,,,,,,\n"
                         "Experiment Name,20210120_LM-GL-HN,,,,,,,,,,\n"
                         "Date,2019-04-09,,,,,,,,,,\n"
                         "Project,New Project,,,,,,,,,,\n"
                         "Workflow,GenerateFASTQ,,,,,,,,,,\n"
                         "[Manifests],,,,,,,,\n"
                         "PoolDNA,MixDNA_Manifest.txt,,,,,,,\n"
                         "PoolRNA,MixRNA_Manifest.txt,,,,,,,\n"
                         "[Reads],,,,,,,,,,,\n"
                         "101,,,,,,,,,,,\n"
                         "101,,,,,,,,,,,\n"
                         "[Settings],,,,,,,,,,,\n"
                         "Adapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,,,,,\n"
                         "AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,,,,,\n"
                         "Read1UMILength,7,,,,,,,,,,\n"
                         "Read2UMILength,7,,,,,,,,,,\n"
                         "Read1StartFromCycle,9,,,,,,,,,,\n"
                         "Read2StartFromCycle,9,,,,,,,,,,\n"
                         "[Data],,,,,,,,,,,\n"
                         "Lane,Sample_ID,index,index2,Sample_Name,Sample_Plate,Sample_Well,"
                         "I7_Index_ID,I5_Index_ID,Project,Description,Manifest\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [('R21-2', 'tso500', ',R21-2,ACTGCTTA,AGAGGCGC,,,,D716,D511,RNA,AP13,PoolRNA\n'),
                         ('R21-3', 'tso500', ',R21-3,ATGCGGCT,TAGCCGCG,,,,D714,D512,RNA,AP14,PoolRNA\n'),
                         ('R21-33', 'tso500', ',R21-33,GCCTCTCT,TTCGTAGG,,,,D718,D514,RNA,AP15,PoolRNA\n')])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

    def test_parse_tm(self):
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.tm.csv")
        self.assertEqual("[Header]\n"
                         "Local Run Manager Analysis Id,64064\n"
                         "Experiment Name,TM83\n"
                         "Date,2021-02-08\n"
                         "Module,GenerateFASTQ - 2.0.1\n"
                         "Workflow,GenerateFASTQ\n"
                         "Library Prep Kit,Custom\n"
                         "Chemistry,Amplicon\n"
                         "\n"
                         "[Reads]\n"
                         "151\n"
                         "151\n"
                         "\n"
                         "[Settings]\n"
                         "Read1UMILength,3\n"
                         "Read2UMILength,3\n"
                         "Read1StartFromCycle,6\n"
                         "Read2StartFromCycle,6\n"
                         "\n"
                         "[Data]\n"
                         "Sample_ID,Sample_Name,Description,index,I7_Index_ID,index2,I5_Index_ID,Sample_Project\n",
                         result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'], [])
        self.maxDiff = None
        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [
            ('56063', 'tm', '56063,56063,NA_NA_NA_83_CGU-2020-12,GTGAAGTG,GTGAAGTG,GAGCAATC,GAGCAATC,TM\n'),
            ('FD99-00078', 'tm', 'FD99-00078,FD99-00078,NA_NA_NA_83_CGU-2017-5,CATGGCTA,CATGGCTA,CACACATC,CACACATC,TM\n'),
            ('D99-00574', 'tm', 'D99-00574,D99-00574,NA_NA_NA_83_NA,ATGCCTGT,ATGCCTGT,AGATTGCG,AGATTGCG,TM\n'),
            ('D99-00576', 'tm', 'D99-00576,D99-00576,NA_NA_NA_83_NA,CAACACCT,CAACACCT,AGCTACCA,AGCTACCA,TM\n'),
            ('D99-00581', 'tm', 'D99-00581,D99-00581,NA_NA_NA_83_NA,TGTGACTG,TGTGACTG,AGCCTATC,AGCCTATC,TM\n'),
            ('D99-00586', 'tm', 'D99-00586,D99-00586,NA_NA_NA_83_NA,GTCATCGA,GTCATCGA,GATCCACT,GATCCACT,TM\n')

        ])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

    def test_parse_te(self):
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.te.csv")
        self.assertEqual("[Header]\n"
                         "Local Run Manager Analysis Id,63063\n"
                         "Experiment Name,TE42\n"
                         "Date,2021-02-06\n"
                         "Module,GenerateFASTQ - 2.0.1\n"
                         "Workflow,GenerateFASTQ\n"
                         "Library Prep Kit,Custom\n"
                         "Chemistry,Amplicon\n"
                         "\n"
                         "[Reads]\n"
                         "149\n"
                         "149\n"
                         "\n"
                         "[Settings]\n"
                         "\n"
                         "[Data]\n"
                         "Sample_ID,Sample_Name,Description,index,I7_Index_ID,index2,I5_Index_ID,Sample_Project\n",
                         result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'], [])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [
            ("D97-00415", "te", "D97-00415,D97-00415,BIN_M_NA_42_NA,CAACACCGTA,CAACACCGTA,GAACAAGCCG,GAACAAGCCG,TE\n"),
            ("D97-00388", "te", "D97-00388,D97-00388,CAD_K_NA_42_NA,CGAATATTGG,CGAATATTGG,CAGCACGGAA,CAGCACGGAA,TE\n"),
            ("D98-05407", "te", "D98-05407,D98-05407,EXO_K_CGU-2018-16_42_NA,TAATTCCAGC,TAATTCCAGC,ATCGTATTCG,ATCGTATTCG,TE\n")
        ])



    def test_contains_haloplex(self):
        self.assertTrue(contains("wp1","sera","tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertFalse(contains("wp1","tso500","tests/samplesheets/files/SampleSheet.haloplex.csv"))


    def test_parse_tso500(self):
        self.assertTrue(contains("wp1","tso500","tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertFalse(contains("wp1","sera","tests/samplesheets/files/SampleSheet.tso500.csv"))

    def test_parse_tm(self):
        self.assertTrue(contains("wp2","tm","tests/samplesheets/files/SampleSheet.tm.csv"))
        self.assertFalse(contains("wp1","sera","tests/samplesheets/files/SampleSheet.tm.csv"))

    def test_parse_te(self):
        self.assertTrue(contains("wp3","te","tests/samplesheets/files/SampleSheet.te.csv"))
        self.assertFalse(contains("wp2","tm","tests/samplesheets/files/SampleSheet.te.csv"))


if __name__ == '__main__':
    unittest.main()
