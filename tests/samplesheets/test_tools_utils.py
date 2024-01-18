import unittest
from ductus.tools.utils import extract_analysis_information
from ductus.tools.utils import contains
from ductus.tools.utils import get_experiments
from ductus.tools.utils import get_project_and_experiment
from ductus.tools.utils import get_project_types
from ductus.tools.utils import get_samples
from ductus.tools.utils import get_samples_and_info
from ductus.tools.utils import generate_elastic_statistics


class TestUtils(unittest.TestCase):

    def test_parse_samplesheet_v2(self):
        self.maxDiff = None
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.v2.csv")
        self.assertEqual("FileFormatVersion,2,,\n"
                         "RunName,MyRun,,\n"
                         "Date,20230607\n"
                         "InstrumentPlatform,NextSeq1k2k,,\n"
                         "InstrumentType,NextSeq2000,,\n"
                         ",,,\n"
                         "[Reads],,,\n"
                         "Read1Cycles,125,,\n"
                         "Read2Cycles,125,,\n"
                         "Index1Cycles,8,,\n"
                         "Index2Cycles,8,,\n"
                         ",,,\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [('20-2500', '20230607-LU', '20230607', 'SERA',
                           'K1%Desc1', '20-2500,K1%Desc1,WP1_SERA_20230607-LU\n'),
                         ('20-2501', '20230607-LU', '20230607', 'SERA',
                          'K1%Desc2', '20-2501,K1%Desc2,WP1_SERA_20230607-LU\n'),
                         ('20-2502', '20230607-LA', '20230607', 'GMS560',
                          'K1%Desc3', '20-2502,K1%Desc3,WP1_GMS560_20230607-LA\n')])

        self.assertEqual(result['wp2']['forskning'], [])
        self.assertEqual(result['wp2']['projekt'], [])
        self.assertEqual(result['wp2']['utveckling'], [])
        self.assertEqual(result['wp2']['klinik'],
                         [('D99-00581', 'TM83', '20230607', 'TM',
                           'K1%NA_K2%NA_K3%NA_K4%83_K5%NA', 'D99-00581,K1%NA_K2%NA_K3%NA_K4%83_K5%NA,WP2_TM_TM83\n'),
                          ('D99-00586', 'TM83', '20230607', 'TM',
                           'K1%NA_K2%NA_K3%NA_K4%83_K5%NA', 'D99-00586,K1%NA_K2%NA_K3%NA_K4%83_K5%NA,WP2_TM_TM83\n')])

        self.assertEqual(result['wp3']['forskning'], [])
        self.assertEqual(result['wp3']['projekt'], [])
        self.assertEqual(result['wp3']['utveckling'], [])
        self.assertEqual(result['wp3']['klinik'],
                         [('D98-05407', 'TE42', '20230607', 'TE', 'K1%EXO_K2%K_K3%CGU-2018-16_K4%42_K5%NA',
                           'D98-05407,K1%EXO_K2%K_K3%CGU-2018-16_K4%42_K5%NA,WP3_TE_TE42\n'),
                          ('D98-05408', 'TE42', '20230607', 'TE', 'K1%EXO_K2%K_K3%CGU-2018-16_K4%42_K5%NA',
                           'D98-05408,K1%EXO_K2%K_K3%CGU-2018-16_K4%42_K5%NA,WP3_TE_TE42\n')])

    def test_parse_haloplex(self):
        result = extract_analysis_information("tests/samplesheets/files/SampleSheet.haloplex.csv")

        self.assertEqual("[Header]\n"
                         "Local Run Manager Analysis Id,56056\n"
                         "Experiment Name,20210203-LU\n"
                         "Date,2021-02-04\n"
                         "Module,GenerateFASTQ - 2.0.0\n"
                         "Workflow,GenerateFASTQ\n"
                         "Library Prep Kit,HaloPlex\n"
                         "Chemistry,Default\n"
                         "\n"
                         "[Reads]\n"
                         "151\n"
                         "151\n"
                         "\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [('97-181', '20210203-LU', '20210204', 'sera', '',
                           '97-181,97-181,,ACCTCCAA,E03,WP1_SERA_20210203-LU\n'),
                         ('97-217', '20210203-LU', '20210204', 'sera', '',
                          '97-217,97-217,,GCGAGTAA,F03,WP1_SERA_20210203-LU\n'),
                         ('97-218', '20210203-LU', '20210204', 'sera', '',
                          '97-218,97-218,,ACTATGCA,G03,WP1_SERA_20210203-LU\n'),
                         ('97-219', '20210203-LU', '20210204', 'sera', '',
                          '97-219,97-219,,CGGATTGC,H03,WP1_SERA_20210203-LU\n'),
                         ('97-220', '20210203-LU', '20210204', 'sera', '',
                          '97-220,97-220,,AACTCACC,A04,WP1_SERA_20210203-LU\n'),
                         ('97-221', '20210203-LU', '20210204', 'sera', '',
                          '97-221,97-221,,GCTAACGA,B04,WP1_SERA_20210203-LU\n')])

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
                         "\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [('20-2500', '20201221-LU', "20201223", 'sera', '',
                           '20-2500,20-2500,CACTTCGA,D01,,,,WP1_SERA_20201221-LU\n'),
                         ('20-2501', '20201221-LU', "20201223", 'sera', '',
                          '20-2501,20-2501,GCCAAGAC,E01,,,,WP1_SERA_20201221-LU\n')])

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
                         ",,,,,,,,,\n", result['header'])

        self.assertEqual(result['wp1']['forskning'], [])
        self.assertEqual(result['wp1']['projekt'], [])
        self.assertEqual(result['wp1']['utveckling'], [])
        self.assertEqual(result['wp1']['klinik'],
                         [('21-399', '20210302-MS', '20210303', 'sera', '',
                           '21-399,21-399,,,D701,ATTACTCG,D502,ATAGAGGC,WP1_SERA_20210302-MS,\n'),
                         ('21-417', '20210302-MS', '20210303', 'sera', '',
                          '21-417,21-417,,,D702,TCCGGAGA,D502,ATAGAGGC,WP1_SERA_20210302-MS,\n')])

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
                         "Read2StartFromCycle,9,,,,,,,,,,\n", result['header'])

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
                                ',R21-2,ACTGCTTA,AGAGGCGC,,,,D716,D511,WP1_TSO500_20190409-LM-GL-HN,AP13,PoolRNA\n'
                            ),
                            (
                                'R21-3',
                                '20190409-LM-GL-HN',
                                "20190409",
                                'tso500',
                                'AP14',
                                ',R21-3,ATGCGGCT,TAGCCGCG,,,,D714,D512,WP1_TSO500_20190409-LM-GL-HN,AP14,PoolRNA\n'
                            ),
                            (
                                'R21-33',
                                '20190409-LM-GL-HN',
                                "20190409",
                                'tso500',
                                'AP15',
                                ',R21-33,GCCTCTCT,TTCGTAGG,,,,D718,D514,WP1_TSO500_20190409-LM-GL-HN,AP15,PoolRNA\n'
                            ),
                            (
                                '21-33',
                                '20190409-LM-GL-HN',
                                "20190409",
                                'tso500',
                                'UP15',
                                ',21-33,GCCTCTCT,TTCGTAGG,,,,D718,D514,WP1_TSO500_20190409-LM-GL-HN,UP15,0.2\n'
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
                         "Experiment Name,20221025-MS,,,,,,,,,\n"
                         "Date,20221025,,,,,,,,,\n"
                         "Project,New Project,,,,,,,,,\n"
                         "Workflow,GenerateFASTQ,,,,,,,,,\n"
                         "[Reads],,,,,,,,,,\n"
                         "151,,,,,,,,,,\n"
                         "151,,,,,,,,,,\n"
                         "[Settings],,,,,,,,,,\n"
                         "AdapterRead1,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,,,,\n"
                         "AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,,,,\n"
                         "OverrideCycles,U3N2Y146;I8;I8;U3N2Y146,,,,,,,,,\n", result['header'])

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
                                'xGen_UDI_Index1',
                                '22-2427,CTGATCGT,GCGCATAT,,,,,,WP1_GMS560_20221025-MS,xGen_UDI_Index1,0.7\n'
                            ),
                            (
                                '22-2428',
                                '20221025-MS',
                                "20221025",
                                'gms560',
                                'xGen_UDI_Index2',
                                '22-2428,ACTCTCGA,CTGTACCA,,,,,,WP1_GMS560_20221025-MS,xGen_UDI_Index2,0.6\n'
                            ),
                            (
                                'R22-2429',
                                '20221025-MS',
                                "20221025",
                                'gms560',
                                'xGen_UDI_Index3',
                                'R22-2429,TGAGCTAG,GAACGGTT,,,,,,WP1_GMS560_20221025-MS,xGen_UDI_Index3,\n'
                            ),
                            (
                                'R22-2430',
                                '20221025-MS',
                                "20221025",
                                'gms560',
                                'xGen_UDI_Index4',
                                'R22-2430,GAGACGAT,ACCGGTTA,,,,,,WP1_GMS560_20221025-MS,xGen_UDI_Index4,\n'
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
                         "\n",
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
                               "K1%NA_K2%NA_K3%NA_K4%42_K5%NA",
                               "R99-00277,R99-00277,K1%NA_K2%NA_K3%NA_K4%42_K5%NA,TAGGCATG,"
                               "TAGGCATG,AGAGTAGA,AGAGTAGA,WP2_ABL_BCRABL42\n"
                            ),
                            (
                               "R99-00255",
                               "BCRABL42",
                               "20230324",
                               "abl",
                               "K1%NA_K2%NA_K3%NA_K4%42_K5%NA",
                               "R99-00255,R99-00255,K1%NA_K2%NA_K3%NA_K4%42_K5%NA,TAGGCATG,"
                               "TAGGCATG,GCGTAAGA,GCGTAAGA,WP2_ABL_BCRABL42\n"
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
                         "\n", result['header'])

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
                                'K1%NA_K2%NA_K3%NA_K4%83_K5%CGU-2020-12',
                                '56063,56063,K1%NA_K2%NA_K3%NA_K4%83_K5%CGU-2020-12,GTGAAGTG,'
                                'GTGAAGTG,GAGCAATC,GAGCAATC,WP2_TM_TM83\n'
                            ),
                            (
                                'FD99-00078',
                                'TM83',
                                '20210208',
                                'tm',
                                'K1%NA_K2%NA_K3%NA_K4%83_K5%CGU-2017-5',
                                'FD99-00078,FD99-00078,K1%NA_K2%NA_K3%NA_K4%83_K5%CGU-2017-5,CATGGCTA,'
                                'CATGGCTA,CACACATC,CACACATC,WP2_TM_TM83\n'
                            ),
                            (
                                'D99-00574',
                                'TM83',
                                '20210208',
                                'tm',
                                'K1%NA_K2%NA_K3%NA_K4%83_K5%NA',
                                'D99-00574,D99-00574,K1%NA_K2%NA_K3%NA_K4%83_K5%NA,ATGCCTGT,'
                                'ATGCCTGT,AGATTGCG,AGATTGCG,WP2_TM_TM83\n'
                            ),
                            (
                                'D99-00576',
                                'TM83',
                                '20210208',
                                'tm',
                                'K1%NA_K2%NA_K3%NA_K4%83_K5%NA',
                                'D99-00576,D99-00576,K1%NA_K2%NA_K3%NA_K4%83_K5%NA,CAACACCT,'
                                'CAACACCT,AGCTACCA,AGCTACCA,WP2_TM_TM83\n'
                            ),
                            (
                                'D99-00581',
                                'TM83',
                                '20210208',
                                'tm',
                                'K1%NA_K2%NA_K3%NA_K4%83_K5%NA',
                                'D99-00581,D99-00581,K1%NA_K2%NA_K3%NA_K4%83_K5%NA,TGTGACTG,'
                                'TGTGACTG,AGCCTATC,AGCCTATC,WP2_TM_TM83\n'
                            ),
                            (
                                'D99-00586',
                                'TM83',
                                '20210208',
                                'tm',
                                'K1%NA_K2%NA_K3%NA_K4%83_K5%NA',
                                'D99-00586,D99-00586,K1%NA_K2%NA_K3%NA_K4%83_K5%NA,GTCATCGA,'
                                'GTCATCGA,GATCCACT,GATCCACT,WP2_TM_TM83\n'
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
                         "\n", result['header'])

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
                                'K1%BIN_K2%M_K3%NA_K4%42_K5%NA',
                                "D97-00415,D97-00415,K1%BIN_K2%M_K3%NA_K4%42_K5%NA,CAACACCGTA,"
                                "CAACACCGTA,GAACAAGCCG,GAACAAGCCG,WP3_TE_TE42\n"
                            ),
                            (
                                "D97-00388",
                                'TE42',
                                '20210206',
                                "te",
                                'K1%CAD_K2%K_K3%NA_K4%42_K5%NA',
                                "D97-00388,D97-00388,K1%CAD_K2%K_K3%NA_K4%42_K5%NA,CGAATATTGG,"
                                "CGAATATTGG,CAGCACGGAA,CAGCACGGAA,WP3_TE_TE42\n"
                            ),
                            (
                                "D98-05407",
                                'TE42',
                                '20210206',
                                "te",
                                'K1%EXO_K2%K_K3%CGU-2018-16_K4%42_K5%NA',
                                "D98-05407,D98-05407,K1%EXO_K2%K_K3%CGU-2018-16_K4%42_K5%NA,TAATTCCAGC,TAATTCCAGC,"
                                "ATCGTATTCG,ATCGTATTCG,WP3_TE_TE42\n"
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
                         "\n", result['header'])

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
                                "K1%NA_K2%NA_K3%NA_K4%42_K5%NA",
                                "D99-06299,D99-06299,K1%NA_K2%NA_K3%NA_K4%42_K5%NA,GGCCTTGTTA,"
                                "GGCCTTGTTA,GTGTTCCACG,GTGTTCCACG,WP3_TC_TC42\n"
                             ),
                             (
                                "D99-01027",
                                "TC42",
                                "20211103",
                                "tc",
                                "K1%NA_K2%NA_K3%NA_K4%42_K5%NA",
                                "D99-01027,D99-01027,K1%NA_K2%NA_K3%NA_K4%42_K5%NA,CCTTGTAGCG,"
                                "CCTTGTAGCG,TTGAGCCAGC,TTGAGCCAGC,WP3_TC_TC42\n"
                             )
        ])

    def test_contains_haloplex(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "sera"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "tso500"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "gms560"))

    def test_contains_klinik_haloplex(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "sera", "klinik"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "tso500", "klinik"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "gms560", "klinik"))

    def test_contains_tso500(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.tso500.csv", "wp1", "tso500"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tso500.csv", "wp1", "sera"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tso500.csv", "wp1", "gms560"))

    def test_contains_gms560(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.GMS560.csv", "wp1", "gms560"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.GMS560.csv", "wp1", "sera"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.GMS560.csv", "wp1", "tso500"))

    def test_contains_abl(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.abl.csv", "wp2", "abl"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.abl.csv", "wp1", "sera"))

    def test_contains_tm(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.tm.csv", "wp2", "tm"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tm.csv", "wp1", "sera"))

    def test_contains_te(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.te.csv", "wp3", "te"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.te.csv", "wp2", "tm"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.te.csv", "wp3", "tc"))

    def test_contains_wp3_tc(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.tc.csv", "wp3", "tc"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tc.csv", "wp2", "tm"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.tc.csv", "wp3", "te"))

    def test_get_info_types_haloplex(self):
        self.assertTrue(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "sera"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "tso500"))
        self.assertFalse(contains("tests/samplesheets/files/SampleSheet.haloplex.csv", "wp1", "gms560"))

    def test_info_types(self):
        self.assertEqual(get_project_types("wp1", "sera", "tests/samplesheets/files/SampleSheet.haloplex.csv"), {'klinik', })
        self.assertEqual(get_project_types("wp1", "tso500", "tests/samplesheets/files/SampleSheet.haloplex.csv"), set())
        self.assertEqual(get_project_types("wp1", "gms560", "tests/samplesheets/files/SampleSheet.haloplex.csv"), set())
        self.assertEqual(get_project_types("wp2", "abl", "tests/samplesheets/files/SampleSheet.abl.csv"), {'klinik'})
        self.assertEqual(get_project_types("wp2", "tm", "tests/samplesheets/files/SampleSheet.tm.csv"), {'klinik'})
        self.assertEqual(get_project_types("wp3", "te", "tests/samplesheets/files/SampleSheet.te.csv"), {'klinik'})
        self.assertEqual(get_project_types("wp3", "tc", "tests/samplesheets/files/SampleSheet.tc.csv"), {'klinik'})

    def test_get_project_and_experiment(self):
        self.assertEqual({("klinik", "20210203-LU")},
                         get_project_and_experiment("wp1", "sera", "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual(set(),
                         get_project_and_experiment("wp1", "tso500", "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual({("klinik", "20201221-LU")},
                         get_project_and_experiment("wp1", "sera", "tests/samplesheets/files/SampleSheet.swift.mn.csv"))
        self.assertEqual({("klinik", "20210302-MS")},
                         get_project_and_experiment("wp1", "sera", "tests/samplesheets/files/SampleSheet.swift.m0.csv"))
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
            get_samples_and_info("wp1", "sera", "tests/samplesheets/files/SampleSheet.haloplex.csv"))
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
        self.assertEqual([], get_samples_and_info("wp1", "sera", "tests/samplesheets/files/SampleSheet.tso500.csv"))
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
        self.assertEqual([], get_samples_and_info("wp1", "sera", "tests/samplesheets/files/SampleSheet.GMS560.csv"))
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
                ('D97-00415', 'klinik', 'TE42', '20210206', 'unknown',  'K1%BIN_K2%M_K3%NA_K4%42_K5%NA'),
                ('D97-00388', 'klinik', 'TE42', '20210206', 'unknown',  'K1%CAD_K2%K_K3%NA_K4%42_K5%NA'),
                ('D98-05407', 'klinik', 'TE42', '20210206', 'unknown',  'K1%EXO_K2%K_K3%CGU-2018-16_K4%42_K5%NA')
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
                         get_samples("wp1", "klinik", 'sera', "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual([],
                         get_samples("wp1", "utveckling", 'sera', "tests/samplesheets/files/SampleSheet.haloplex.csv"))
        self.assertEqual(['R21-2', 'R21-3', 'R21-33', '21-33'],
                         get_samples("wp1", "klinik", 'tso500', "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual([],
                         get_samples("wp1", "klinik", 'sera', "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual([],
                         get_samples("wp1", "klinik", 'gms560', "tests/samplesheets/files/SampleSheet.tso500.csv"))
        self.assertEqual(['22-2427', '22-2428', 'R22-2429', 'R22-2430'],
                         get_samples("wp1", "klinik", 'gms560', "tests/samplesheets/files/SampleSheet.GMS560.csv"))
        self.assertEqual([],
                         get_samples("wp1", "klinik", 'sera', "tests/samplesheets/files/SampleSheet.GMS560.csv"))
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
                                                          "sera",
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
                                                              "sera",
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
                                                              'sera',
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
                                                              'sera',
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
                              'experiment.tissue': 'K1%BIN_K2%M_K3%NA_K4%42_K5%NA',
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
                              'experiment.tissue': 'K1%CAD_K2%K_K3%NA_K4%42_K5%NA',
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
                              'experiment.tissue': 'K1%EXO_K2%K_K3%CGU-2018-16_K4%42_K5%NA',
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

    def test_get_experiments(self):
        self.maxDiff = None
        result = get_experiments("tests/samplesheets/files/SampleSheet.v2.csv")
        self.assertEqual({
                          '20230607-LU': {'analysis': 'SERA', 'wp': 'wp1', 'samples': ['20-2500', '20-2501']},
                          '20230607-LA': {'analysis': 'GMS560', 'wp': 'wp1', 'samples': ['20-2502']},
                          'TM83': {'analysis': 'TM', 'wp': 'wp2', 'samples': ['D99-00581', 'D99-00586']},
                          'TE42': {'analysis': 'TE', 'wp': 'wp3', 'samples': ['D98-05407', 'D98-05408']}
                         },
                         result)


if __name__ == '_main_':
    unittest.main()
