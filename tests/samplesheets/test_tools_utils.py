Himport io
import json
import tempfile
import os
import unittest
from ductus.tools.utils import extract_analysis_information
from ductus.tools.utils import contains
from ductus.tools.utils import get_project_and_experiment
from ductus.tools.utils import get_project_types
from ductus.tools.utils import get_samples
from ductus.tools.utils import get_samples_and_info
from ductus.tools.utils import generate_elastic_statistics
from ductus.tools.utils import generate_elastic_statistics_from_api_data
from freezegun import freeze_time


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
                         [('97-181', '20210203-LU', '20210204', 'haloplex-idt', '', '97-181,97-181,,ACCTCCAA,E03,\n', True),
                         ('97-217', '20210203-LU', '20210204', 'haloplex-idt', '', '97-217,97-217,,GCGAGTAA,F03,\n', True),
                         ('97-218', '20210203-LU', '20210204', 'haloplex-idt', '', '97-218,97-218,,ACTATGCA,G03,\n', True),
                         ('97-219', '20210203-LU', '20210204', 'haloplex-idt', '', '97-219,97-219,,CGGATTGC,H03,\n', True),
                         ('97-220', '20210203-LU', '20210204', 'haloplex-idt', '', '97-220,97-220,,AACTCACC,A04,\n', True),
                         ('97-221', '20210203-LU', '20210204', 'haloplex-idt', '', '97-221,97-221,,GCTAACGA,B04,\n', True)])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

    def test_parse_swift(self):
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.swift.mn.csv")

        self.assertEqual("[Header]\n"
                         "Local Run Manager Analysis Id,115115\n"
                         "Date,12/23/2020\n"
                         "Experiment Name,20201221-LU\n"
                         "Workflow,GenerateFastQWorkflow\n"
                         "Description,Auto generated sample sheet.  Used by workflow module to kick off Isis analysis\n"
                         "Chemistry,Amplicon\n"
                         "\n"
                         "[Reads]\n"
                         "151\n"
                         "151\n"
                         "\n"
                         "[Data]\n"
                         "Sample_ID,Sample_Name,index,I7_Index_ID,index2,I5_Index_ID,Description\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [('20-2500', '20201221-LU', "20201223", 'haloplex-idt', '', '20-2500,20-2500,CACTTCGA,D01,,,\n', True),
                         ('20-2501', '20201221-LU', "20201223", 'haloplex-idt', '', '20-2501,20-2501,GCCAAGAC,E01,,,\n', True)])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.swift.m0.csv")
        self.assertEqual("[Header],,,,,,,,,\n"
                         "IEMFileVersion,4,,,,,,,,\n"
                         "Experiment Name,20210302-MS,,,,,,,,\n"
                         "Date,2021-03-03,,,,,,,,\n"
                         "Workflow,GenerateFASTQ,,,,,,,,\n"
                         "Application,FASTQ Only,,,,,,,,\n"
                         "Assay,TruSeq HT,,,,,,,,\n"
                         "Description,,,,,,,,,\n"
                         "Chemistry,Amplicon,,,,,,,,\n"
                         ",,,,,,,,,\n"
                         "[Reads],,,,,,,,,\n"
                         "151,,,,,,,,,\n"
                         "151,,,,,,,,,\n"
                         ",,,,,,,,,\n"
                         "[Settings],,,,,,,,,\n"
                         "ReverseComplement,0,,,,,,,,\n"
                         "Adapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,,,\n"
                         "AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,,,\n"
                         ",,,,,,,,,\n"
                         "[Data],,,,,,,,,\n"
                         "Sample_ID,Sample_Name,Sample_Plate,Sample_Well,I7_Index_ID,index,I5_Index_ID"
                         ",index2,Sample_Project,Description\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [('21-399', '20210302-MS', '20210303', 'haloplex-idt', '',
                           '21-399,21-399,,,D701,ATTACTCG,D502,ATAGAGGC,,\n', True),
                         ('21-417', '20210302-MS', '20210303', 'haloplex-idt', '',
                          '21-417,21-417,,,D702,TCCGGAGA,D502,ATAGAGGC,,\n', True)])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

    def test_parse_tso(self):
        self.maxDiff = None
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.tso500.csv")
        self.assertEqual("[Header],,,,,,,,,,,\n"
                         "IEMFileVersion,4,,,,,,,,,,\n"
                         "Investigator Name,,,,,,,,,,,\n"
                         "Experiment Name,20190409-LM-GL-HN,,,,,,,,,,\n"
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
                         "I7_Index_ID,I5_Index_ID,Project,Description,TC\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [
                            (
                                'R21-2',
                                '20190409-LM-GL-HN',
                                "20190409",
                                'tso500',
                                'AP13',
                                ',R21-2,ACTGCTTA,AGAGGCGC,,,,D716,D511,RNA,AP13,PoolRNA\n',
                                True
                            ),
                            (
                                'R21-3',
                                '20190409-LM-GL-HN',
                                "20190409",
                                'tso500',
                                'AP14',
                                ',R21-3,ATGCGGCT,TAGCCGCG,,,,D714,D512,RNA,AP14,PoolRNA\n',
                                True
                            ),
                            (
                                'R21-33',
                                '20190409-LM-GL-HN',
                                "20190409",
                                'tso500',
                                'AP15',
                                ',R21-33,GCCTCTCT,TTCGTAGG,,,,D718,D514,RNA,AP15,PoolRNA\n',
                                True
                            ),
                            (
                                '21-33',
                                '20190409-LM-GL-HN',
                                "20190409",
                                'tso500',
                                'UP15',
                                ',21-33,GCCTCTCT,TTCGTAGG,,,,D718,D514,DNA,UP15,0.2\n',
                                True
                            )
                        ])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

    def test_parse_gms560(self):
        self.maxDiff = None
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.GMS560.csv")
        self.assertEqual("[Header],,,,,,,,,,\n"
                         "IEMFileVersion,4,,,,,,,,,\n"
                         "Investigator Name,,,,,,,,,,\n"
                         "Experiment Name,20221025_MS,,,,,,,,,\n"
                         "Date,20221025,,,,,,,,,\n"
                         "Project,New Project,,,,,,,,,\n"
                         "Workflow,GenerateFASTQ,,,,,,,,,\n"
                         "[Reads],,,,,,,,,,\n"
                         "151,,,,,,,,,,\n"
                         "151,,,,,,,,,,\n"
                         "[Settings],,,,,,,,,,\n"
                         "AdapterRead1,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,,,,\n"
                         "AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,,,,\n"
                         "OverrideCycles,U3N2Y146;I8;I8;U3N2Y146,,,,,,,,,\n"
                         "[Data],,,,,,,,,,\n"
                         "Sample_ID,index,index2,Sample_Name,Sample_Plate,Sample_Well,"
                         "I7_Index_ID,I5_Index_ID,Project,Description,TC\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [
                            (
                                '22-2427',
                                '20221025-MS',
                                "20221025",
                                'gms560',
                                'tumor_content:0.7',
                                '22-2427,CTGATCGT,GCGCATAT,,,,,DNA,xGen_UDI_Index1,tumor_content:0.7\n',
                                True
                            ),
                            (
                                '22-2428',
                                '20221025-MS',
                                "20221025",
                                'gms560',
                                'tumor_content:0.6',
                                '22-2428,ACTCTCGA,CTGTACCA,,,,,DNA,xGen_UDI_Index2,tumor_content:0.6\n',
                                True
                            ),
                            (
                                'R22-2429',
                                '20221025-MS',
                                "20221025",
                                'gms560',
                                '',
                                'R22-2429,TGAGCTAG,GAACGGTT,,,,,RNA,xGen_UDI_Index3,\n',
                                True
                            ),
                            (
                                'R22-2430',
                                '20221025-MS',
                                "20221025",
                                'gms560',
                                '',
                                'R22-2430,GAGACGAT,ACCGGTTA,,,,,RNA,xGen_UDI_Index4,\n',
                                True
                            )
                        ])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'], [])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

    def test_parse_abl(self):
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.abl.csv")
        self.assertEqual("[Header]\n"
                         "Local Run Manager Analysis Id,123123\n"
                         "Experiment Name,BCRABL42\n"
                         "Date,2023-03-24\n"
                         "Module,GenerateFASTQ - 3.0.1\n"
                         "Workflow,GenerateFASTQ\n"
                         "Library Prep Kit,Custom\n"
                         "Index Kit,Custom\n"
                         "Chemistry,Amplicon\n"
                         "\n"
                         "[Reads]\n"
                         "151\n"
                         "151\n"
                         "\n"
                         "[Settings]\n"
                         "\n"
                         "[Data]\n"
                         "Sample_ID,Sample_Name,Description,I7_Index_ID,index,I5_Index_ID,index2,Sample_Project\n",
                         result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'], [])
        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'],
                         [
                            (
                               "R99-00277",
                               "BCRABL42",
                               "20230324",
                               "abl",
                               "NA_NA_NA_42_NA",
                               "R99-00277,R99-00277,NA_NA_NA_42_NA,TAGGCATG,TAGGCATG,AGAGTAGA,AGAGTAGA,ABL\n",
                               True
                            ),
                            (
                               "R99-00255",
                               "BCRABL42",
                               "20230324",
                               "abl",
                               "NA_NA_NA_42_NA",
                               "R99-00255,R99-00255,NA_NA_NA_42_NA,TAGGCATG,TAGGCATG,GCGTAAGA,GCGTAAGA,ABL\n",
                               True
                            )
                         ])
        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'], [])

    def test_parse_tm(self):
        self.maxDiff = None
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
        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'],
                         [
                            (
                                '56063',
                                'TM83',
                                '20210208',
                                'tm',
                                'NA_NA_NA_83_CGU-2020-12',
                                '56063,56063,NA_NA_NA_83_CGU-2020-12,GTGAAGTG,GTGAAGTG,GAGCAATC,GAGCAATC,TM\n',
                                True
                            ),
                            (
                                'FD99-00078',
                                'TM83',
                                '20210208',
                                'tm',
                                'NA_NA_NA_83_CGU-2017-5',
                                'FD99-00078,FD99-00078,NA_NA_NA_83_CGU-2017-5,CATGGCTA,CATGGCTA,CACACATC,CACACATC,TM\n',
                                True
                            ),
                            (
                                'D99-00574',
                                'TM83',
                                '20210208',
                                'tm',
                                'NA_NA_NA_83_NA',
                                'D99-00574,D99-00574,NA_NA_NA_83_NA,ATGCCTGT,ATGCCTGT,AGATTGCG,AGATTGCG,TM\n',
                                True
                            ),
                            (
                                'D99-00576',
                                'TM83',
                                '20210208',
                                'tm',
                                'NA_NA_NA_83_NA',
                                'D99-00576,D99-00576,NA_NA_NA_83_NA,CAACACCT,CAACACCT,AGCTACCA,AGCTACCA,TM\n',
                                True
                            ),
                            (
                                'D99-00581',
                                'TM83',
                                '20210208',
                                'tm',
                                'NA_NA_NA_83_NA',
                                'D99-00581,D99-00581,NA_NA_NA_83_NA,TGTGACTG,TGTGACTG,AGCCTATC,AGCCTATC,TM\n',
                                True
                            ),
                            (
                                'D99-00586',
                                'TM83',
                                '20210208',
                                'tm',
                                'NA_NA_NA_83_NA',
                                'D99-00586,D99-00586,NA_NA_NA_83_NA,GTCATCGA,GTCATCGA,GATCCACT,GATCCACT,TM\n',
                                True
                            )
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
        self.assertEqual(result['wp3']['klinik'],
                         [
                            (
                                "D97-00415",
                                'TE42',
                                '20210206',
                                "te",
                                'BIN_M_NA_42_NA',
                                "D97-00415,D97-00415,BIN_M_NA_42_NA,CAACACCGTA,CAACACCGTA,GAACAAGCCG,GAACAAGCCG,TE\n",
                                True
                            ),
                            (
                                "D97-00388",
                                'TE42',
                                '20210206',
                                "te",
                                'CAD_K_NA_42_NA',
                                "D97-00388,D97-00388,CAD_K_NA_42_NA,CGAATATTGG,CGAATATTGG,CAGCACGGAA,CAGCACGGAA,TE\n",
                                True
                            ),
                            (
                                "D98-05407",
                                'TE42',
                                '20210206',
                                "te",
                                'EXO_K_NA_42_CGU-2018-16',
                                "D98-05407,D98-05407,EXO_K_NA_42_CGU-2018-16,TAATTCCAGC,TAATTCCAGC,ATCGTATTCG,ATCGTATTCG,TE\n",
                                True
                            )
        ])

    def test_parse_tc(self):
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.tc.csv")
        self.assertEqual("[Header]\n"
                         "Local Run Manager Analysis Id,10010\n"
                         "Experiment Name,TC42\n"
                         "Date,2021-11-03\n"
                         "Module,GenerateFASTQ - 3.0.1\n"
                         "Workflow,GenerateFASTQ\n"
                         "Library Prep Kit,Custom\n"
                         "Index Kit,Custom\n"
                         "Chemistry,Amplicon\n"
                         "\n"
                         "[Reads]\n"
                         "149\n"
                         "149\n"
                         "\n"
                         "[Settings]\n"
                         "\n"
                         "[Data]\n"
                         "Sample_ID,Sample_Name,Description,I7_Index_ID,index,I5_Index_ID,index2,Sample_Project\n",
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
        self.assertEqual(result['wp3']['klinik'],
                         [
                             (
                                "D99-06299",
                                "TC42",
                                "20211103",
                                "tc",
                                "NA_NA_NA_42_NA",
                                "D99-06299,D99-06299,NA_NA_NA_42_NA,GGCCTTGTTA,GGCCTTGTTA,GTGTTCCACG,GTGTTCCACG,TC\n",
                                True
                             ),
                             (
                                "D99-01027",
                                "TC42",
                                "20211103",
                                "tc",
                                "NA_NA_NA_42_NA",
                                "D99-01027,D99-01027,NA_NA_NA_42_NA,CCTTGTAGCG,CCTTGTAGCG,TTGAGCCAGC,TTGAGCCAGC,TC\n",
                                True
                             )
        ])

    def test_contains_haloplex(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "haloplex-idt"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "tso500"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "gms560"))

    def test_contains_klinik_haloplex(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "haloplex-idt", "klinik"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "tso500", "klinik"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "gms560", "klinik"))

    def test_contains_tso500(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.tso500.csv", "wp1", "tso500"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tso500.csv", "wp1", "haloplex-idt"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tso500.csv", "wp1", "gms560"))

    def test_contains_gms560(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.GMS560.csv", "wp1", "gms560"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.GMS560.csv", "wp1", "haloplex-idt"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.GMS560.csv", "wp1", "tso500"))

    def test_contains_abl(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.abl.csv", "wp2", "abl"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.abl.csv", "wp1", "haloplex-idt"))

    def test_contains_tm(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.tm.csv", "wp2", "tm"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tm.csv", "wp1", "haloplex-idt"))

    def test_contains_te(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.te.csv", "wp3", "te"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.te.csv", "wp2", "tm"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.te.csv", "wp3", "tc"))

    def test_contains_wp3_tc(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.tc.csv", "wp3", "tc"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tc.csv", "wp2", "tm"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tc.csv", "wp3", "te"))

    def test_get_info_types_haloplex(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "haloplex-idt"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "tso500"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "gms560"))

    def test_info_types(self):
        self.assertEqual(get_project_types("wp1", "haloplex-idt", "tests/samplesheets/files/SampleSheet.haloplex.csv"), {'klinik', })
        self.assertEqual(get_project_types("wp1", "tso500", "tests/samplesheets/files/SampleSheet.haloplex.csv"), set())
        self.assertEqual(get_project_types("wp1", "gms560", "tests/samplesheets/files/SampleSheet.haloplex.csv"), set())
        self.assertEqual(get_project_types("wp2", "abl", "tests/samplesheets/files/SampleSheet.abl.csv"), {'klinik'})
        self.assertEqual(get_project_types("wp2", "tm", "tests/samplesheets/files/SampleSheet.tm.csv"), {'klinik'})
        self.assertEqual(get_project_types("wp3", "te", "tests/samplesheets/files/SampleSheet.te.csv"), {'klinik'})
        self.assertEqual(get_project_types("wp3", "tc", "tests/samplesheets/files/SampleSheet.tc.csv"), {'klinik'})

    def test_get_project_and_experiment(self):
        self.assertEqual({("klinik", "20210203-LU")},
                         get_project_and_experiment("wp1", "haloplex-idt", "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual(set(),
                         get_project_and_experiment("wp1", "tso500", "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual({("klinik", "20201221-LU")},
                         get_project_and_experiment("wp1", "haloplex-idt", "tests/samplesheets/files/SampleSheet.swift.mn.csv"))
        self.assertEqual({("klinik", "20210302-MS")},
                         get_project_and_experiment("wp1", "haloplex-idt", "tests/samplesheets/files/SampleSheet.swift.m0.csv"))
        self.assertEqual({("klinik", "20190409-LM-GL-HN")},
                         get_project_and_experiment("wp1", "tso500", "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual({("klinik", "20221025-MS")},
                         get_project_and_experiment("wp1", "gms560", "tests/samplesheets/files/SampleSheet.GMS560.csv"))
        self.assertEqual({("klinik", "BCRABL42")},
                         get_project_and_experiment("wp2", "abl", "tests/samplesheets/files/SampleSheet.abl.csv"))
        self.assertEqual({("klinik", "TM83")},
                         get_project_and_experiment("wp2", "tm", "tests/samplesheets/files/SampleSheet.tm.csv"))
        self.assertEqual({("klinik", "TE42")},
                         get_project_and_experiment("wp3", "te", "tests/samplesheets/files/SampleSheet.te.csv"))
        self.assertEqual({("klinik", "TC42")},
                         get_project_and_experiment("wp3", "tc", "tests/samplesheets/files/SampleSheet.tc.csv"))

    def test_get_samples_info(self):
        self.maxDiff = None
        self.assertEqual(
            [
                ('97-181', 'klinik', '20210203-LU', '20210204', 'LU', 'unknown'),
                ('97-217', 'klinik', '20210203-LU', '20210204', 'LU', 'unknown'),
                ('97-218', 'klinik', '20210203-LU', '20210204', 'LU', 'unknown'),
                ('97-219', 'klinik', '20210203-LU', '20210204', 'LU', 'unknown'),
                ('97-220', 'klinik', '20210203-LU', '20210204', 'LU', 'unknown'),
                ('97-221', 'klinik', '20210203-LU', '20210204', 'LU', 'unknown')
            ],
            get_samples_and_info("wp1", "haloplex-idt", "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual([], get_samples_and_info("wp1", "tso500", "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual([], get_samples_and_info("wp1", "gms560", "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual(
            [
                ('R21-2', 'klinik', '20190409-LM-GL-HN', '20190409', 'LM-GL-HN', 'RNA'),
                ('R21-3', 'klinik', '20190409-LM-GL-HN', '20190409', 'LM-GL-HN', 'RNA'),
                ('R21-33', 'klinik', '20190409-LM-GL-HN', '20190409', 'LM-GL-HN', 'RNA'),
                ('21-33', 'klinik', '20190409-LM-GL-HN', '20190409', 'LM-GL-HN', 'DNA')
            ],
            get_samples_and_info("wp1", "tso500", "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual([], get_samples_and_info("wp1", "haloplex-idt", "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual([], get_samples_and_info("wp1", "gms560", "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual(
            [
                ('22-2427', 'klinik', '20221025-MS', '20221025', 'MS', 'DNA'),
                ('22-2428', 'klinik', '20221025-MS', '20221025', 'MS', 'DNA'),
                ('R22-2429', 'klinik', '20221025-MS', '20221025', 'MS', 'RNA'),
                ('R22-2430', 'klinik', '20221025-MS', '20221025', 'MS', 'RNA')
            ],
            get_samples_and_info("wp1", "gms560", "tests/samplesheets/files/SampleSheet.GMS560.csv"))
        self.assertEqual([], get_samples_and_info("wp1", "tso500", "tests/samplesheets/files/SampleSheet.GMS560.csv"))
        self.assertEqual([], get_samples_and_info("wp1", "haloplex-idt", "tests/samplesheets/files/SampleSheet.GMS560.csv"))
        self.assertEqual(
            [
                ('R99-00277', 'klinik', 'BCRABL42', '20230324', 'unknown', 'RNA'),
                ('R99-00255', 'klinik', 'BCRABL42', '20230324', 'unknown', 'RNA')
            ],
            get_samples_and_info('wp2', 'abl', 'tests/samplesheets/files/SampleSheet.abl.csv'))
        self.assertEqual(
            [
                ('56063', 'klinik', 'TM83', '20210208', 'unknown', 'Hematology'),
                ('FD99-00078', 'klinik', 'TM83', '20210208', 'unknown', 'Hematology'),
                ('D99-00574', 'klinik', 'TM83', '20210208', 'unknown', 'Hematology'),
                ('D99-00576', 'klinik', 'TM83', '20210208', 'unknown', 'Hematology'),
                ('D99-00581', 'klinik', 'TM83', '20210208', 'unknown', 'Hematology'),
                ('D99-00586', 'klinik', 'TM83', '20210208', 'unknown', 'Hematology')
            ],
            get_samples_and_info("wp2", "tm", "tests/samplesheets/files/SampleSheet.tm.csv"))

        self.assertEqual(
            [
                ('D97-00415', 'klinik', 'TE42', '20210206', 'unknown',  'BIN_M_NA_42_NA'),
                ('D97-00388', 'klinik', 'TE42', '20210206', 'unknown',  'CAD_K_NA_42_NA'),
                ('D98-05407', 'klinik', 'TE42', '20210206', 'unknown',  'EXO_K_NA_42_CGU-2018-16')
            ],
            get_samples_and_info("wp3", "te", "tests/samplesheets/files/SampleSheet.te.csv"))

        self.assertEqual(
            [
                ('D99-06299', 'klinik', 'TC42', '20211103', 'unknown', 'Blood'),
                ('D99-01027', 'klinik', 'TC42', '20211103', 'unknown', 'Blood')
            ],
            get_samples_and_info('wp3', 'tc', 'tests/samplesheets/files/SampleSheet.tc.csv'))

    def test_get_samples(self):
        self.assertEqual(["97-181", "97-217", "97-218", "97-219", "97-220", "97-221"],
                         get_samples("wp1", "klinik", 'haloplex-idt', "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual([],
                         get_samples("wp1", "utveckling", 'haloplex-idt', "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual(['R21-2', 'R21-3', 'R21-33', '21-33'],
                         get_samples("wp1", "klinik", 'tso500', "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual([],
                         get_samples("wp1", "klinik", 'haloplex-idt', "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual([],
                         get_samples("wp1", "klinik", 'gms560', "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual(['22-2427', '22-2428', 'R22-2429', 'R22-2430'],
                         get_samples("wp1", "klinik", 'gms560', "tests/samplesheets/files/SampleSheet.GMS560.csv"))
        self.assertEqual([],
                         get_samples("wp1", "klinik", 'haloplex-idt', "tests/samplesheets/files/SampleSheet.GMS560.csv"))
        self.assertEqual([],
                         get_samples("wp1", "klinik", 'tso500', "tests/samplesheets/files/SampleSheet.GMS560.csv"))
        self.assertEqual(['R99-00277', 'R99-00255'],
                         get_samples("wp2", "klinik", "abl", "tests/samplesheets/files/SampleSheet.abl.csv"))
        self.assertEqual(['56063', 'FD99-00078', 'D99-00574', 'D99-00576', 'D99-00581', 'D99-00586'],
                         get_samples("wp2", "klinik", 'tm', "tests/samplesheets/files/SampleSheet.tm.csv"))
        self.assertEqual(['D97-00415', 'D97-00388', 'D98-05407'],
                         get_samples("wp3", "klinik", "te", "tests/samplesheets/files/SampleSheet.te.csv"))
        self.assertEqual(['D99-06299', 'D99-01027'],
                         get_samples("wp3", "klinik", "tc", "tests/samplesheets/files/SampleSheet.tc.csv"))

    def test_generate_elastic_statistics(self):
        self.maxDiff = None
        self.assertCountEqual(generate_elastic_statistics("tests/samplesheets/files/SampleSheet.haloplex.csv",
                                                          "wp1",
                                                          "haloplex-idt",
                                                          'haloplex',
                                                          "klinik",
                                                          "ffpe"),
                              [
                                {
                                    '@timestamp': '2021-02-04T01:01:01.000Z',
                                    'experiment.id': '20210203-LU',
                                    'experiment.method': 'haloplex',
                                    'experiment.prep': 'ffpe',
                                    'experiment.project': 'klinik',
                                    'experiment.rerun': False,
                                    'experiment.sample': '97-181',
                                    'experiment.tissue': 'unknown',
                                    'experiment.user': 'LU',
                                    'experiment.wp': 'WP1'
                                },
                                {
                                    '@timestamp': '2021-02-04T01:01:01.000Z',
                                    'experiment.id': '20210203-LU',
                                    'experiment.method': 'haloplex',
                                    'experiment.prep': 'ffpe',
                                    'experiment.project': 'klinik',
                                    'experiment.rerun': False,
                                    'experiment.sample': '97-217',
                                    'experiment.tissue': 'unknown',
                                    'experiment.user': 'LU',
                                    'experiment.wp': 'WP1'
                                },
                                {
                                    '@timestamp': '2021-02-04T01:01:01.000Z',
                                    'experiment.id': '20210203-LU',
                                    'experiment.method': 'haloplex',
                                    'experiment.prep': 'ffpe',
                                    'experiment.project': 'klinik',
                                    'experiment.rerun': False,
                                    'experiment.sample': '97-218',
                                    'experiment.tissue': 'unknown',
                                    'experiment.user': 'LU',
                                    'experiment.wp': 'WP1'
                                },
                                {
                                    '@timestamp': '2021-02-04T01:01:01.000Z',
                                    'experiment.id': '20210203-LU',
                                    'experiment.method': 'haloplex',
                                    'experiment.prep': 'ffpe',
                                    'experiment.project': 'klinik',
                                    'experiment.rerun': False,
                                    'experiment.sample': '97-219',
                                    'experiment.tissue': 'unknown',
                                    'experiment.user': 'LU',
                                    'experiment.wp': 'WP1'
                                },
                                {
                                    '@timestamp': '2021-02-04T01:01:01.000Z',
                                    'experiment.id': '20210203-LU',
                                    'experiment.method': 'haloplex',
                                    'experiment.prep': 'ffpe',
                                    'experiment.project': 'klinik',
                                    'experiment.rerun': False,
                                    'experiment.sample': '97-220',
                                    'experiment.tissue': 'unknown',
                                    'experiment.user': 'LU',
                                    'experiment.wp': 'WP1'
                                },
                                {
                                    '@timestamp': '2021-02-04T01:01:01.000Z',
                                    'experiment.id': '20210203-LU',
                                    'experiment.method': 'haloplex',
                                    'experiment.prep': 'ffpe',
                                    'experiment.project': 'klinik',
                                    'experiment.rerun': False,
                                    'experiment.sample': '97-221',
                                    'experiment.tissue': 'unknown',
                                    'experiment.user': 'LU',
                                    'experiment.wp': 'WP1'
                                }]
                              )
        self.assertCountEqual([], generate_elastic_statistics("tests/samplesheets/files/SampleSheet.haloplex.csv",
                                                              "wp1",
                                                              "haloplex-idt",
                                                              "haloplex",
                                                              "utveckling",
                                                              'ffpe'))
        self.assertCountEqual([
                            {
                                '@timestamp': '2019-04-09T01:01:01.000Z',
                                'experiment.id': '20190409-LM-GL-HN',
                                'experiment.method': 'TSO500',
                                'experiment.prep': 'FFPE',
                                'experiment.project': 'klinik',
                                'experiment.rerun': False,
                                'experiment.sample': 'R21-2',
                                'experiment.tissue': 'RNA',
                                'experiment.user': 'LM-GL-HN',
                                'experiment.wp': 'WP1'
                            },
                            {
                                '@timestamp': '2019-04-09T01:01:01.000Z',
                                'experiment.id': '20190409-LM-GL-HN',
                                'experiment.method': 'TSO500',
                                'experiment.prep': 'FFPE',
                                'experiment.project': 'klinik',
                                'experiment.rerun': False,
                                'experiment.sample': 'R21-3',
                                'experiment.tissue': 'RNA',
                                'experiment.user': 'LM-GL-HN',
                                'experiment.wp': 'WP1'
                            },
                            {
                                '@timestamp': '2019-04-09T01:01:01.000Z',
                                'experiment.id': '20190409-LM-GL-HN',
                                'experiment.method': 'TSO500',
                                'experiment.prep': 'FFPE',
                                'experiment.project': 'klinik',
                                'experiment.rerun': False,
                                'experiment.sample': 'R21-33',
                                'experiment.tissue': 'RNA',
                                'experiment.user': 'LM-GL-HN',
                                'experiment.wp': 'WP1'
                            },
                            {
                                '@timestamp': '2019-04-09T01:01:01.000Z',
                                'experiment.id': '20190409-LM-GL-HN',
                                'experiment.method': 'TSO500',
                                'experiment.prep': 'FFPE',
                                'experiment.project': 'klinik',
                                'experiment.rerun': False,
                                'experiment.sample': '21-33',
                                'experiment.tissue': 'DNA',
                                'experiment.user': 'LM-GL-HN',
                                'experiment.wp': 'WP1'
                            }],
                         generate_elastic_statistics("tests/samplesheets/files/SampleSheet.tso500.csv",
                                                     "wp1",
                                                     'tso500',
                                                     'TSO500',
                                                     "klinik",
                                                     'FFPE'))
        self.assertCountEqual([], generate_elastic_statistics("tests/samplesheets/files/SampleSheet.tso500.csv",
                                                              "wp1",
                                                              'haloplex-idt',
                                                              'TSO500',
                                                              "klinik",
                                                              'plasma'))

        self.assertCountEqual([
                            {
                                '@timestamp': '2022-10-25T01:01:01.000Z',
                                'experiment.id': '20221025-MS',
                                'experiment.method': 'gms560',
                                'experiment.prep': 'FFPE',
                                'experiment.project': 'klinik',
                                'experiment.rerun': False,
                                'experiment.sample': '22-2427',
                                'experiment.tissue': 'DNA',
                                'experiment.user': 'MS',
                                'experiment.wp': 'WP1'
                            },
                            {
                                '@timestamp': '2022-10-25T01:01:01.000Z',
                                'experiment.id': '20221025-MS',
                                'experiment.method': 'gms560',
                                'experiment.prep': 'FFPE',
                                'experiment.project': 'klinik',
                                'experiment.rerun': False,
                                'experiment.sample': '22-2428',
                                'experiment.tissue': 'DNA',
                                'experiment.user': 'MS',
                                'experiment.wp': 'WP1'
                            },
                            {
                                '@timestamp': '2022-10-25T01:01:01.000Z',
                                'experiment.id': '20221025-MS',
                                'experiment.method': 'gms560',
                                'experiment.prep': 'FFPE',
                                'experiment.project': 'klinik',
                                'experiment.rerun': False,
                                'experiment.sample': 'R22-2429',
                                'experiment.tissue': 'RNA',
                                'experiment.user': 'MS',
                                'experiment.wp': 'WP1'
                            },
                            {
                                '@timestamp': '2022-10-25T01:01:01.000Z',
                                'experiment.id': '20221025-MS',
                                'experiment.method': 'gms560',
                                'experiment.prep': 'FFPE',
                                'experiment.project': 'klinik',
                                'experiment.rerun': False,
                                'experiment.sample': 'R22-2430',
                                'experiment.tissue': 'RNA',
                                'experiment.user': 'MS',
                                'experiment.wp': 'WP1'
                            }],
                         generate_elastic_statistics("tests/samplesheets/files/SampleSheet.GMS560.csv",
                                                     "wp1",
                                                     'gms560',
                                                     'gms560',
                                                     "klinik",
                                                     'FFPE'))
        self.assertCountEqual([], generate_elastic_statistics("tests/samplesheets/files/SampleSheet.GMS560.csv",
                                                              "wp1",
                                                              'haloplex-idt',
                                                              'gms560',
                                                              "klinik",
                                                              'plasma'))
        self.assertCountEqual([], generate_elastic_statistics("tests/samplesheets/files/SampleSheet.GMS560.csv",
                                                              "wp1",
                                                              'tso500',
                                                              'gms560',
                                                              "klinik",
                                                              'plasma'))

        self.assertCountEqual([
                                 {
                                     '@timestamp': '2023-03-24T01:01:01.000Z',
                                     'experiment.id': 'BCRABL42',
                                     'experiment.method': 'BCR_ABL1',
                                     'experiment.prep': 'Nextera',
                                     'experiment.project': 'klinik',
                                     'experiment.rerun': False,
                                     'experiment.sample': 'R99-00277',
                                     'experiment.tissue': 'RNA',
                                     'experiment.user': 'unknown',
                                     'experiment.wp': 'WP2'
                                 },
                                 {
                                     '@timestamp': '2023-03-24T01:01:01.000Z',
                                     'experiment.id': 'BCRABL42',
                                     'experiment.method': 'BCR_ABL1',
                                     'experiment.prep': 'Nextera',
                                     'experiment.project': 'klinik',
                                     'experiment.rerun': False,
                                     'experiment.sample': 'R99-00255',
                                     'experiment.tissue': 'RNA',
                                     'experiment.user': 'unknown',
                                     'experiment.wp': 'WP2'
                                 }],
                              generate_elastic_statistics("tests/samplesheets/files/SampleSheet.abl.csv",
                                                          "wp2",
                                                          'abl',
                                                          'BCR_ABL1',
                                                          "klinik",
                                                          "Nextera"))

        self.assertCountEqual([
                                 {
                                     '@timestamp': '2021-02-08T01:01:01.000Z',
                                     'experiment.id': 'TM83',
                                     'experiment.method': 'Twist_Myeloid',
                                     'experiment.prep': 'Fresh',
                                     'experiment.project': 'klinik',
                                     'experiment.rerun': False,
                                     'experiment.sample': '56063',
                                     'experiment.tissue': 'Hematology',
                                     'experiment.user': 'unknown',
                                     'experiment.wp': 'WP2'
                                 },
                                 {
                                     '@timestamp': '2021-02-08T01:01:01.000Z',
                                     'experiment.id': 'TM83',
                                     'experiment.method': 'Twist_Myeloid',
                                     'experiment.prep': 'Fresh',
                                     'experiment.project': 'klinik',
                                     'experiment.rerun': False,
                                     'experiment.sample': 'FD99-00078',
                                     'experiment.tissue': 'Hematology',
                                     'experiment.user': 'unknown',
                                     'experiment.wp': 'WP2'
                                 },
                                 {
                                     '@timestamp': '2021-02-08T01:01:01.000Z',
                                     'experiment.id': 'TM83',
                                     'experiment.method': 'Twist_Myeloid',
                                     'experiment.prep': 'Fresh',
                                     'experiment.project': 'klinik',
                                     'experiment.rerun': False,
                                     'experiment.sample': 'D99-00576',
                                     'experiment.tissue': 'Hematology',
                                     'experiment.user': 'unknown',
                                     'experiment.wp': 'WP2'
                                 },
                                 {
                                     '@timestamp': '2021-02-08T01:01:01.000Z',
                                     'experiment.id': 'TM83',
                                     'experiment.method': 'Twist_Myeloid',
                                     'experiment.prep': 'Fresh',
                                     'experiment.project': 'klinik',
                                     'experiment.rerun': False,
                                     'experiment.sample': 'D99-00581',
                                     'experiment.tissue': 'Hematology',
                                     'experiment.user': 'unknown',
                                     'experiment.wp': 'WP2'
                                 },
                                 {
                                     '@timestamp': '2021-02-08T01:01:01.000Z',
                                     'experiment.id': 'TM83',
                                     'experiment.method': 'Twist_Myeloid',
                                     'experiment.prep': 'Fresh',
                                     'experiment.project': 'klinik',
                                     'experiment.rerun': False,
                                     'experiment.sample': 'D99-00586',
                                     'experiment.tissue': 'Hematology',
                                     'experiment.user': 'unknown',
                                     'experiment.wp': 'WP2'
                                 },
                                 {
                                     '@timestamp': '2021-02-08T01:01:01.000Z',
                                     'experiment.id': 'TM83',
                                     'experiment.method': 'Twist_Myeloid',
                                     'experiment.prep': 'Fresh',
                                     'experiment.project': 'klinik',
                                     'experiment.rerun': False,
                                     'experiment.sample': 'D99-00574',
                                     'experiment.tissue': 'Hematology',
                                     'experiment.user': 'unknown',
                                     'experiment.wp': 'WP2'
                                 }],
                              generate_elastic_statistics("tests/samplesheets/files/SampleSheet.tm.csv",
                                                          "wp2",
                                                          'tm',
                                                          'Twist_Myeloid',
                                                          "klinik",
                                                          "Fresh"))
        self.assertCountEqual([
                          {
                              '@timestamp': '2021-02-06T01:01:01.000Z',
                              'experiment.id': 'TE42',
                              'experiment.method': 'TWIST',
                              'experiment.prep': 'TWIST',
                              'experiment.project': 'klinik',
                              'experiment.rerun': False,
                              'experiment.sample': 'D97-00415',
                              'experiment.tissue': 'BIN_M_NA_42_NA',
                              'experiment.user': 'unknown',
                              'experiment.wp': 'WP3'
                          },
                          {
                              '@timestamp': '2021-02-06T01:01:01.000Z',
                              'experiment.id': 'TE42',
                              'experiment.method': 'TWIST',
                              'experiment.prep': 'TWIST',
                              'experiment.project': 'klinik',
                              'experiment.rerun': False,
                              'experiment.sample': 'D97-00388',
                              'experiment.tissue': 'CAD_K_NA_42_NA',
                              'experiment.user': 'unknown',
                              'experiment.wp': 'WP3'
                          },
                          {
                              '@timestamp': '2021-02-06T01:01:01.000Z',
                              'experiment.id': 'TE42',
                              'experiment.method': 'TWIST',
                              'experiment.prep': 'TWIST',
                              'experiment.project': 'klinik',
                              'experiment.rerun': False,
                              'experiment.sample': 'D98-05407',
                              'experiment.tissue': 'EXO_K_NA_42_CGU-2018-16',
                              'experiment.user': 'unknown',
                              'experiment.wp': 'WP3'
                          }],
                       generate_elastic_statistics("tests/samplesheets/files/SampleSheet.te.csv",
                                                   "wp3",
                                                   "te",
                                                   "TWIST",
                                                   "klinik",
                                                   'TWIST'))
        self.assertEqual([
                    {
                        '@timestamp': '2021-11-03T01:01:01.000Z',
                        'experiment.id': 'TC42',
                        'experiment.method': 'TWIST Cancer',
                        'experiment.prep': 'TWIST',
                        'experiment.project': 'klinik',
                        'experiment.rerun': False,
                        'experiment.sample': 'D99-06299',
                        'experiment.tissue': 'Blood',
                        'experiment.user': 'unknown',
                        'experiment.wp': 'WP3'
                    },
                    {
                        '@timestamp': '2021-11-03T01:01:01.000Z',
                        'experiment.id': 'TC42',
                        'experiment.method': 'TWIST Cancer',
                        'experiment.prep': 'TWIST',
                        'experiment.project': 'klinik',
                        'experiment.rerun': False,
                        'experiment.sample': 'D99-01027',
                        'experiment.tissue': 'Blood',
                        'experiment.user': 'unknown',
                        'experiment.wp': 'WP3'
                    }],
                    generate_elastic_statistics("tests/samplesheets/files/SampleSheet.tc.csv",
                                                "wp3",
                                                "tc",
                                                "TWIST Cancer",
                                                "klinik",
                                                "TWIST"))

    @freeze_time("2023-02-01 12:00:00")
    def test_generate_elastic_statistics_from_api(self):
        self.maxDiff = None
        data = json.load(open("tests/samplesheets/files/samples_and_settings_gms560.json"))
        self.assertEqual(generate_elastic_statistics_from_api_data(data),
                         [
                                {
                                    'experiment.wp': 'wp1',
                                    'experiment.prep': 'NA',
                                    '@timestamp': '2023-02-01T01:01:01.000Z',
                                    'experiment.method': 'gms560',
                                    'experiment.rerun': False,
                                    'experiment.user': 'NA',
                                    'experiment.tissue': 'T',
                                    'experiment.id': '20221108_MS-HN-LM',
                                    'experiment.sample': '22-2427',
                                    'experiment.project': 'klinik',
                                },
                                {
                                    'experiment.wp': 'wp1',
                                    'experiment.prep': 'NA',
                                    '@timestamp': '2023-02-01T01:01:01.000Z',
                                    'experiment.method': 'gms560',
                                    'experiment.rerun': False,
                                    'experiment.user': 'NA',
                                    'experiment.tissue': 'T',
                                    'experiment.id': '20221108_MS-HN-LM',
                                    'experiment.sample': '22-2428',
                                    'experiment.project': 'klinik',
                                },
                                {
                                    'experiment.wp': 'wp1',
                                    'experiment.prep': 'NA',
                                    '@timestamp': '2023-02-01T01:01:01.000Z',
                                    'experiment.method': 'gms560',
                                    'experiment.rerun': False,
                                    'experiment.user': 'NA',
                                    'experiment.tissue': 'R',
                                    'experiment.id': '20221108_MS-HN-LM',
                                    'experiment.sample': 'R22-2429',
                                    'experiment.project': 'klinik',
                                },
                                {
                                    'experiment.wp': 'wp1',
                                    'experiment.prep': 'NA',
                                    '@timestamp': '2023-02-01T01:01:01.000Z',
                                    'experiment.method': 'gms560',
                                    'experiment.rerun': False,
                                    'experiment.user': 'NA',
                                    'experiment.tissue': 'R',
                                    'experiment.id': '20221108_MS-HN-LM',
                                    'experiment.sample': 'R22-2430',
                                    'experiment.project': 'klinik',
                                }
                            ])

    def test_old_or_new_format(self):
        from ductus.tools.utils import is_old_ductus_format
        old_format = [
            "tests/samplesheets/files/SampleSheet.abl.csv",
            "tests/samplesheets/files/SampleSheet.GMS560.csv",
            "tests/samplesheets/files/SampleSheet.haloplex.csv",
            "tests/samplesheets/files/SampleSheet.swift.m0.csv",
            "tests/samplesheets/files/SampleSheet.swift.mn.csv",
            "tests/samplesheets/files/SampleSheet.tc.csv",
            "tests/samplesheets/files/SampleSheet.te.csv",
            "tests/samplesheets/files/SampleSheet.tm.csv",
        ]

        for old_file in old_format:
            match_old_format_only = is_old_ductus_format(old_file)
            if not match_old_format_only:
                print(old_file)
            self.assertTrue(match_old_format_only)

        new_format = [
            "tests/samplesheets/files/SampleSheet.abl.newcgformat.csv",
            "tests/samplesheets/files/SampleSheet.GMS560.newcgformat.csv",
            "tests/samplesheets/files/SampleSheet.haloplex.newcgformat.csv",
            "tests/samplesheets/files/SampleSheet.tc.newcgformat.csv",
            "tests/samplesheets/files/SampleSheet.te.newcgformat.csv",
            "tests/samplesheets/files/SampleSheet.tm.newcgformat.csv",
        ]

        for new_file in new_format:
            match_old_format_only = is_old_ductus_format(new_file)
            if match_old_format_only:
                print(new_file)
            self.assertFalse(match_old_format_only)

    def test_convert_old_cgu_format_to_new(self):
        from ductus.tools.utils import convert_old_cgu_samplesheet_format_to_new
        self.maxDiff = None

        with tempfile.TemporaryDirectory() as temp_dir:
            old_samplesheet_cg_format = "tests/samplesheets/files/SampleSheet.GMS560.csv"
            expected_new_samplesheet_cg_format = "tests/samplesheets/files/SampleSheet.GMS560.newcgformat.csv"
            new_samplesheet = os.path.join(temp_dir, "new_samplesheet.csv")
            convert_old_cgu_samplesheet_format_to_new(old_samplesheet_cg_format, new_samplesheet)
            with open(new_samplesheet, 'r') as f1, open(expected_new_samplesheet_cg_format, 'r') as f2:
                generated_lines = f1.readlines()
                expected_lines = f2.readlines()
                self.assertEqual(generated_lines, expected_lines)

    def test_create_analysis_file_from_samplesheet(self):
        from ductus.tools.utils import create_analysis_file, detect_encoding

        self.maxDiff = None
        gms560 = "tests/samplesheets/files/SampleSheet.GMS560.csv"
        gms560_expected_analysis = "tests/analysis/20221025-MS_analysis.csv"
        sera = "tests/samplesheets/files/SampleSheet.haloplex.csv"
        sera_expected_analysis = "tests/analysis/20210203-LU_analysis.csv"
        tc = "tests/samplesheets/files/SampleSheet.tc.csv"
        tc_expected_analysis = "tests/analysis/TC42_analysis.csv"
        te = "tests/samplesheets/files/SampleSheet.te.csv"
        te_expected_analysis = "tests/analysis/TE42_analysis.csv"
        tm = "tests/samplesheets/files/SampleSheet.tm.csv"
        tm_expected_analysis = "tests/analysis/TM83_analysis.csv"

        with tempfile.TemporaryDirectory() as temp_dir:
            file_created = create_analysis_file(gms560, temp_dir)
            self.assertEqual(open(file_created[0]).read(), open(gms560_expected_analysis).read())
            file_created = create_analysis_file(sera, temp_dir)
            self.assertEqual(io.open(file_created[0]).read(),
                             io.open(sera_expected_analysis, encoding=detect_encoding(sera_expected_analysis)).read())
            file_created = create_analysis_file(tc, temp_dir)
            self.assertEqual(open(file_created[0]).read(), open(tc_expected_analysis).read())
            file_created = create_analysis_file(tm, temp_dir)
            self.assertEqual(open(file_created[0]).read(), open(tm_expected_analysis).read())
            file_created = create_analysis_file(te, temp_dir)
            self.assertEqual(open(file_created[0]).read(), open(te_expected_analysis).read())

    def test_combine_sample_and_files(self):
        from ductus.tools.utils import combine_files_with_samples
        self.maxDiff = None

        sample_list = [('S1', 'E1'), ('S2', 'E2'), ('S3', 'E3')]
        file_list = ['path/S1_test_f.R1.fastq.gz', 'path/S2_test_f.R1.fastq.gz',
                     'path/S2_test_f.R2.fastq.gz', 'path/S1_test_f.R2.fastq.gz',
                     'path/E3_S3_test_f1.R1.fastq.gz', 'path/E3_S3_test_f1.R2.fastq.gz',
                     'path/E3_S3_test_f2.R1.fastq.gz', 'path/E3_S3_test_f.R2.fastq.gz']

        self.assertEqual([
            ('S1', 'E1', 'path/S1_test_f.R1.fastq.gz'),
            ('S1', 'E1', 'path/S1_test_f.R2.fastq.gz'),
            ('S2', 'E2', 'path/S2_test_f.R1.fastq.gz'),
            ('S2', 'E2', 'path/S2_test_f.R2.fastq.gz'),
            ('S3', 'E3', 'path/E3_S3_test_f1.R1.fastq.gz'),
            ('S3', 'E3', 'path/E3_S3_test_f1.R2.fastq.gz'),
            ('S3', 'E3', 'path/E3_S3_test_f2.R1.fastq.gz'),
            ('S3', 'E3', 'path/E3_S3_test_f.R2.fastq.gz')
        ], combine_files_with_samples(sample_list, file_list.copy()))

        with self.assertRaises(Exception) as context:
            combine_files_with_samples(sample_list[1:], file_list.copy())
        self.assertTrue(str(context.exception).startswith("Couldn't match file path"))

        with self.assertRaises(Exception) as e:
            combine_files_with_samples(sample_list, [file_list[0]] + file_list[3:])
        self.assertEqual(str(e.exception), "No fastq files found for S2, E2")

        log_message = []
        with self.assertLogs() as log_message:
            combine_files_with_samples(sample_list, file_list[1:])
        self.assertTrue(log_message.output[0].startswith("WARNING:root:Un-even number of fastq"))

    def test_create_json_update(self):
        from ductus.tools.utils import create_json_update_fastq
        from ductus.tools.utils import combine_files_with_samples
        self.maxDiff = None

        sample_list = [('S1', 'E1'), ('S2', 'E2'), ('S3', 'E3')]
        file_list = ['path/S1_test_f.R1.fastq.gz',
                     'path/S2_test_f.R1.fastq.gz',
                     'path/S2_test_f.R2.fastq.gz',
                     'path/S1_test_f.R2.fastq.gz',
                     'path/E3_S3_test_f1.R1.fastq.gz',
                     'path/E3_S3_test_f1.R2.fastq.gz',
                     'path/E3_S3_test_f2.R1.fastq.gz',
                     'path/E3_S3_test_f.R2.fastq.gz']

        result_list = combine_files_with_samples(sample_list, file_list)

        self.assertEqual(
            create_json_update_fastq(result_list),
            {'add': [
                {'experiment': 'E1', 'path': 'path/S1_test_f.R1.fastq.gz', 'sample': 'S1'},
                {'experiment': 'E1', 'path': 'path/S1_test_f.R2.fastq.gz', 'sample': 'S1'},
                {'experiment': 'E2', 'path': 'path/S2_test_f.R1.fastq.gz', 'sample': 'S2'},
                {'experiment': 'E2', 'path': 'path/S2_test_f.R2.fastq.gz', 'sample': 'S2'},
                {'experiment': 'E3', 'path': 'path/E3_S3_test_f1.R1.fastq.gz', 'sample': 'S3'},
                {'experiment': 'E3', 'path': 'path/E3_S3_test_f1.R2.fastq.gz', 'sample': 'S3'},
                {'experiment': 'E3', 'path': 'path/E3_S3_test_f2.R1.fastq.gz', 'sample': 'S3'},
                {'experiment': 'E3', 'path': 'path/E3_S3_test_f.R2.fastq.gz', 'sample': 'S3'}]})


if __name__ == '__main__':
    unittest.main()
