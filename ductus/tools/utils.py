import cchardet
import datetime
import glob
import io
import json
import os
import re
import logging


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = cchardet.detect(raw_data)
    encoding = result['encoding']
    return encoding


def generate_elastic_statistics(samplesheet, workpackage, tool, analysis, project, prep):
    data = get_samples_and_info(workpackage, tool, samplesheet)
    samples = []
    for d in data:
        if project == d[1]:
            samples.append(
                ({
                  "experiment.wp": workpackage.upper(),
                  "experiment.prep": prep,
                  "@timestamp": datetime.datetime.strptime(d[3], "%Y%m%d").strftime('%Y-%m-%dT01:01:01.000Z'),
                  "experiment.method": analysis,
                  "experiment.rerun": False,
                  "experiment.user": d[4],
                  "experiment.tissue": d[5],
                  "experiment.id": d[2],
                  "experiment.sample": d[0],
                  "experiment.project": d[1]
                }))

    return samples


def generate_elastic_statistics_from_api_data(data):
    samples = []
    for sample in data['samples']:
        samples.append(
            ({
                "experiment.wp": data["samples"][sample]["workpackage"],
                "experiment.prep": data["samples"][sample]["settings"].get('prep', 'NA'),
                "@timestamp": datetime.datetime.now().strftime('%Y-%m-%dT01:01:01.000Z'),
                "experiment.method": data["samples"][sample]["analysis"],
                "experiment.rerun": False,
                "experiment.user": data["samples"][sample]["settings"].get('user', 'NA'),
                "experiment.tissue": data["samples"][sample]["settings"].get('type', 'NA'),
                "experiment.id": data["samples"][sample]["analysis_name"],
                "experiment.sample": sample,
                "experiment.project": data["samples"][sample]["settings"].get('project', 'klinik'),
            }))
    return samples


def contains(samplesheet, workpackage=None, analysis=None, project=None):
    data = extract_analysis_information(samplesheet)
    if workpackage in data:
        for type, analyzes in data[workpackage].items():
            if project is None or type == project:
                for a_item in analyzes:
                    if analysis is None or analysis in a_item:
                        return True
    return False


def get_samples(workpackage, project, analysis, samplesheet):
    data = extract_analysis_information(samplesheet)
    sample = []
    if workpackage in data:
        for project_type, data in data[workpackage].items():
            if project == project_type:
                for d in data:
                    if analysis in d:
                        sample.append(d[0])
    return sample


def print_samples(workpackage, project, analysis, samplesheet):
    print(*get_samples(workpackage, project, analysis, samplesheet), sep="\n")


def get_samples_and_project(workpackage, analysis, samplesheet):
    import warnings
    warnings.warn(
                  "get_samples_and_project will be deprecated, use get_samples_and_info instead",
                  PendingDeprecationWarning
        )
    return get_samples_and_info(workpackage, analysis, samplesheet)


def is_old_ductus_format(samplesheet):
    new_format = False
    s_data = extract_analysis_information(samplesheet)
    from pprint import pprint
    old_format = False
    new_format = False
    for wp in s_data:
        if wp.startswith("wp"):
            for _, data in s_data[wp].items():
                for d in data:
                    if d[-1]:
                        old_format = True
                    else:
                        new_format = True
    if old_format and new_format:
        raise Exception("Can not handle both new and old samplesheet format")

    return old_format


def convert_old_cgu_samplesheet_format_to_new(samplesheet, new_file):
    """
    New SampleSheet format will require the Sample_Id to be built up by experiment id and sample id,
    EXPERIMENT-ID_SAMPLEID, example TE42_45-61561.
    """
    with open(new_file, "w") as writer:
        s_data = extract_analysis_information(samplesheet)
        tc_column_found = False
        if "TC" in s_data['header']:
            tc_column_found = True
            s_data['header'] = s_data['header'].replace(',TC\n', '\n')
        writer.write(s_data['header'])
        for wp in s_data:
            if wp.startswith("wp"):
                for _, data in s_data[wp].items():
                    for d in data:
                        # Replace old Sample_Id format with new version
                        new_samplesheet_format = f"{d[1]}_{d[0]}"
                        writer.write(d[-2].replace(d[0], new_samplesheet_format))


def create_analysis_file(samplesheet, outputfolder):
    def create_description(wp, data, sample, analysis, index_file=None):
        """
        Convert old SampleSheet description to new version. Old version contain
        values separated by '_' and WP1 had a separate columnd for TC. New
        format will contain key and values, seperated by ':', where each key:value item
        is separated by '%'. Ex K1:V1%K2:V2%K3:V3
        """
        index_data = None
        if index_file and analysis == "haloplex-idt":
            """
            If an index file has been provided this is a haloplex-idt analysis which will need this file
            in later analysis steps. It will therefore be saved to description, as a header and
            data section.
            """
            header = None
            data = None
            with io.open(index_file, mode="r", encoding=detect_encoding(index_file)) as reader:
                header = next(reader).rstrip().replace(",", ";")
                if "Experimentnamn" not in header:
                    raise Exception(f"No head found in {index_file}")
                for row in reader:
                    if sample in row:
                        data = row.rstrip().replace(",", ";").split(";")
                        data[0] = data[0].replace('_', '-')
                        data = ";".join(data)
                        break
            if data is None:
                raise Exception("Couldn't match sample with index file")
            else:
                index_data = f"index_header:{header}%index_data:{data}"
        if "wp1" == wp:
            description = ""
            if re.search(r"tumor_content:[10]+\.[0-9]+", data) or re.search(r"type:[TRAU]+", data):
                """
                Detect tumor content value. Note that ductus-core moved it to description
                when parsing the SampleSheet.
                """
                description = data
            if index_data:
                # Add index data if it exist.
                if description:
                    description += description + "%" + index_data
                else:
                    description = index_data
            return description
        elif wp in ["wp2", "wp3"]:
            """
            ToDo: WP2 and WP3 should update this part to match there requirements.
            """
            keys = ['panel', 'sex', 'trio', 'experiment', 'project']
            return "%".join(map(lambda v: f"{v[0]}:{v[1]}", zip(keys, data.split('_'))))
        elif "wp3":
            return "wp3"

    s_data = extract_analysis_information(samplesheet)
    files_created = []
    for wp in s_data:
        if wp.startswith("wp"):
            for _, data in s_data[wp].items():
                if data:
                    files_created.append(os.path.join(outputfolder, f"{data[0][1]}_analysis.csv"))
                    base_path = os.path.dirname(samplesheet)
                    file = glob.glob(f"{base_path}/*ndex.csv")
                    if len(file) > 0:
                        file = file[0]
                    else:
                        file = None
                    with open(files_created[-1], 'w') as writer:
                        writer.write(",".join(["Workpackage", "Experiment", "Analysis", "Sample_ID", "Description"]))
                        for d in data:
                            writer.write('\n' + ','.join([wp, d[1], d[3], d[0], create_description(wp, d[4], d[0], d[3], file)]))
    return files_created


def get_samples_and_info(workpackage, analysis, samplesheet):
    data = extract_analysis_information(samplesheet)
    sample_project = []
    if workpackage in data:
        for project_type, data in data[workpackage].items():
            for d in data:
                if analysis in d:
                    user = "unknown"
                    tissue = "unknown"
                    if workpackage.lower() == "wp1":
                        user = "-".join(d[1].split("-")[1:])
                        if analysis.lower() == "tso500" or analysis.lower() == "gms560":
                            tissue = "RNA" if d[0].startswith("R") else "DNA"
                    elif workpackage.lower() == "wp2" and analysis.lower() == "tm":
                        tissue = "Hematology"
                    elif workpackage.lower() == "wp2" and analysis.lower() == "abl":
                        tissue = "RNA"
                    elif workpackage.lower() == "wp3" and analysis.lower() == "te":
                        tissue = d[4]
                    elif workpackage.lower() == "wp3" and analysis.lower() == "tc":
                        tissue = "Blood"

                    sample_project.append((d[0], project_type, d[1], d[2], user, tissue))
    return sample_project


def get_project_types(workpackage, analysis, samplesheet):
    data = extract_analysis_information(samplesheet)
    project_types = []
    if workpackage in data:
        for project_type, analyzes in data[workpackage].items():
            for a_item in analyzes:
                if analysis in a_item:
                    project_types.append(project_type)
    return set(project_types)


def get_project_and_experiment(workpackage, analysis, samplesheet):
    data = extract_analysis_information(samplesheet)
    project_and_analysis = []
    if workpackage in data:
        for project_type, analyzes in data[workpackage].items():
            for a_item in analyzes:
                if analysis in a_item:
                    project_and_analysis.append((project_type, a_item[1]))
    return set(project_and_analysis)


def print_project_types(workpackage, analysis, samplesheet):
    print(*get_project_types(workpackage, analysis, samplesheet), sep="\n")


def extract_analysis_information(samplesheet):
    """
        Function used to extract samples from a SampleSheet.csv and group them after
        workpackage and project type, example Klinik,s
    """
    with open(samplesheet) as file:
        pattern = re.compile(r"experiment name,\d{8}[_-][a-z0-9-]+")
        sera = False
        tso500 = False
        gms560 = False
        TM = False
        ABL = False
        TE = False
        TC = False
        data = {'header': "",
                'wp1': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []},
                'wp2': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []},
                'wp3': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []},
                'wpN': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []}}
        date_string = None
        main_experiment = None
        for line in file:
            data['header'] = data['header'] + line
            if line.startswith("Date"):
                if "/" in line:
                    date_result = re.search(r"Date,(\d{1,2})/(\d{1,2})/(\d{4})", line)
                    date_string = "{}{:02d}{:02d}".format(date_result[3], int(date_result[1]), int(date_result[2]))
                else:
                    date_result = re.search(r"^Date,(\d{4})-{0,1}(\d{1,2})-{0,1}(\d{1,2})", line)
                    date_string = "{}{:02d}{:02d}".format(date_result[1], int(date_result[2]), int(date_result[3]))
            if line.startswith("Experiment Name,"):
                main_experiment = re.search("^Experiment Name,([A-Za-z0-9_-]+)", line)[1]
            line = line.lower()

            if pattern.search(line):
                sera = True
            if "name,te" in line:
                TE = True
            if "name,tm" in line:
                TM = True
            if "name,bcrabl" in line:
                ABL = True
            if "name,tc" in line:
                TC = True
            if line.startswith("[data]"):
                line = next(file)
                if "description,tc" in line.lower():
                    tso500 = True
                    sera = False
                    if "lane" not in line.lower():
                        gms560 = True
                        tso500 = False
                data['header'] = data['header'] + line
                header_map = {v[1].lower(): v[0] for v in enumerate(re.split(",|;", line.rstrip()))}
                for row in file:
                    columns = re.split(",|;", row.rstrip())

                    if len(columns) <= 1:
                        continue
                    description = ""
                    if 'description' in header_map:
                        description = columns[header_map['description']]
                    if gms560:
                        """
                        Move tc/tumor_content to description to make it easier to convert old
                        samplesheet to new format. And remove tc column from row.
                        """

                        # existing description will be added later for gms560
                        description = ""
                        if 'tc' in header_map and len(columns[header_map['tc']].rstrip()) > 0:
                            description = "tumor_content:" + columns[header_map['tc']].rstrip()
                        elif 'tumor_content' in header_map and len(columns[header_map['tc']].rstrip()) > 0:
                            description = "tumor_content:" + columns[header_map['tumor_content']].rstrip()
                        if len(columns[header_map['tc']].rstrip()) > 0:
                            row = re.sub(r',[0-9.]+$', '', row)
                        else:
                            row = re.sub(r',$', '', row)
                        if 'project' in header_map and len(columns[header_map['project']].rstrip()) > 0:
                            if len(description) > 0:
                                description += "%"
                            if columns[header_map['project']].lower() == "dna":
                                description += "type:T"
                            elif columns[header_map['project']].lower() == "rna":
                                description += "type:R"
                            else:
                                description += "type:U"
                        elif 'sample_project' in header_map and len(columns[header_map['sample_project']].rstrip()) > 0:
                            if len(description) > 0:
                                description += "%"
                            if columns[header_map['sample_project']].lower() == "dna":
                                description += "type:T"
                            elif columns[header_map['sample_project']].lower() == "rna":
                                description += "type:R"
                            else:
                                description += "type:U"
                        else:
                            description += "type:U"

                        columns = row.split(",")
                        columns[header_map['description']] = columns[header_map['description']].rstrip()
                        if columns[header_map['description']]:
                            columns[header_map['description']] = "oldDescription:" + columns[header_map['description']] + \
                                                                 "%" + description
                        else:
                            columns[header_map['description']] = description
                        columns[header_map['description']] += "\n"
                        row = ",".join(columns)

                    sample_id = columns[header_map['sample_id']]
                    sample_experiment = main_experiment
                    old_format = True
                    if "_" in sample_id:
                        sample_experiment, sample_id = sample_id.split("_")
                        old_format = False
                    if not old_format:
                        data["wpN"]['klinik'].append((sample_id,
                                                      sample_experiment,
                                                      date_string,
                                                      "N",
                                                      description,
                                                      row,
                                                      old_format))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("tm"):
                        data["wp2"]['klinik'].append((sample_id,
                                                      sample_experiment,
                                                      date_string,
                                                      "tm",
                                                      description,
                                                      row,
                                                      old_format))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("abl"):
                        data["wp2"]['klinik'].append((sample_id,
                                                      sample_experiment,
                                                      date_string,
                                                      "abl",
                                                      description,
                                                      row,
                                                      old_format))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("te"):
                        data["wp3"]['klinik'].append((sample_id,
                                                      sample_experiment,
                                                      date_string,
                                                      "te",
                                                      description,
                                                      row,
                                                      old_format))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("tc"):
                        data["wp3"]['klinik'].append((sample_id,
                                                      sample_experiment,
                                                      date_string,
                                                      "tc",
                                                      description,
                                                      row,
                                                      old_format))
                    else:
                        if tso500:
                            data["wp1"]['klinik'].append((sample_id,
                                                          sample_experiment.replace('_', '-'),
                                                          date_string,
                                                          "tso500",
                                                          description,
                                                          row,
                                                          old_format))
                        elif sera:
                            data["wp1"]['klinik'].append((sample_id,
                                                          sample_experiment.replace('_', '-'),
                                                          date_string,
                                                          "haloplex-idt",
                                                          description,
                                                          row,
                                                          old_format))
                        elif gms560:
                            data["wp1"]['klinik'].append((sample_id,
                                                          sample_experiment.replace('_', '-'),
                                                          date_string,
                                                          "gms560",
                                                          description,
                                                          row,
                                                          old_format))
                        else:
                            raise Exception("Unhandled case: " + row)
        return data


def extract_wp_and_typo(samplesheet):
    """
        Function used to extract samples from a SampleSheet.csv and group them after
        workpackage and project type, example Klinik,s
    """
    with open(samplesheet) as file:
        pattern = re.compile(r"experiment name,\d{8}_[a-z0-9-]+")
        haloplex = False
        tso500 = False
        gms560 = False
        TM = False
        ABL = False
        TE = False
        TC = False
        for line in file:
            line = line.lower()
            if pattern.search(line):
                sera = True
            if "name,te" in line:
                TE = True
            if "name,tm" in line:
                TM = True
            if "name,bcrabl" in line:
                ABL = True
            if "name,tc" in line:
                TC = True
            if line.startswith("[data]"):
                line = next(file)
                if "description,tc" in line.lower():
                    tso500 = True
                    sera = False
                    if "lane" not in line.lower():
                        gms560 = True
                        tso500 = False
                break
        return (('haloplex', haloplex), ('tso500', tso500), ('gms560', gms560), ('te', TE), ('tm', TM), ('abl', ABL), ('tc', TC))


def combine_files_with_samples(sample_list, file_list, force_paired_sequence_files=False):
    """
        The function takes three inputs:
         - a list of tuples, containing sample id and experiment id
         - a list of files
         - a boolean indicating whether the function should fail if the samples do not contain paired reads

         It will attempt to match files to the provided sample/experiment
         information and return a new list of tuples containing (sample_id, experiment_id, file).
         If a file can't be matched to a sample, an exception will be raised. If a
         sample isn't assigned any files, an exception will be raised. A warning will be
         generated if a sample does not have an even number of files assigned. If
         force_paired_sequence_files is set to true, the function will fail instead.

         The expected file format is either experiment-id_sample-id or just sample-id
    """
    sample_dict = dict(map(lambda sample_info: (sample_info[0], {'experiment_id': sample_info[1], 'file_list': []}), sample_list))
    for f in file_list[:]:
        file_name = os.path.basename(f).split('_')
        if file_name[1] in sample_dict and sample_dict[file_name[1]]['experiment_id'] == file_name[0]:
            sample_dict[file_name[1]]['file_list'].append(f)
            file_list.remove(f)
        elif file_name[0] in sample_dict:
            sample_dict[file_name[0]]['file_list'].append(f)
            file_list.remove(f)
        elif "Undetermined" in file_name[0]:
            file_list.remove(f)
        else:
            raise Exception(f"Couldn't match file {f} with sample list {sample_list}")

    if len(file_list) > 0:
        raise Exception("Couldn't match all fastq files to a sample")
    result_list = []
    for sample in sample_dict:
        if not sample_dict[sample]['file_list']:
            logging.debug(f"No fastq files found for {sample}, {sample_dict[sample]['experiment_id']}")
            raise Exception(f"No fastq files found for {sample}, {sample_dict[sample]['experiment_id']}")
        elif len(sample_dict[sample]['file_list']) % 2 != 0:
            if force_paired_sequence_files:
                raise Exception(f"Un-even number of fastq files found for sample {sample}")
            else:
                logging.warning(f"Un-even number of fastq files found for sample {sample}, "
                                f"{sample_dict[sample]['experiment_id']}, files {sample_dict[sample]['file_list']}")
        for f in sample_dict[sample]['file_list']:
            result_list.append((sample, sample_dict[sample]['experiment_id'], f))
    return result_list


def create_json_update_fastq(sample_list, operation='add'):
    return {operation: list(map(lambda info: dict(zip(('sample', 'experiment', 'path'), info)), sample_list))}


def filter_experiment(sample_sheet_file):
    """
        This function uses a path to a bioinformatic samples sheet and read it as a string to sort out the experiment name
        for the current run being processed. The file will be converted to a list to separate rows in
        to distinct items. A list of known patterns is provided inside the function and each
        row from the sample sheet will be compared with all known patterns. If a match is found the
        function will return True and if no mathc was found the return value will be False.
        In further processing this means that a return value equal to False should continue
        the processing of the current run and that a return value of True should end the processing.
        param sample_sheet_string: string
        return: boolean
    """
    with open(sample_sheet_file) as file:
        sample_sheet_list = file.readlines()

    filter_out = [".*[Ll]ymphotrack.*",
                  "DC",
                  "AH",
                  ]
    experiment_match = []
    for exp in filter_out:
        experiment_name = r'^[Ee]xperiment [Nn]ame,{}'.format(exp)
        pattern = re.compile(experiment_name)
        experiment_match = experiment_match + list(filter(pattern.match, sample_sheet_list))

    if not experiment_match:
        # No match will give an empty list.
        return False
    else:
        return True


def get_nr_expected_fastqs(sample_sheet_file, file_list):
    """
        This function uses the information in a sample sheet to calculate the expected
        number of fastq-files that should be transferred from the instrument to
        the hospital file area. It uses the lane information, if available, from the sample sheet.
        The number of expected fastq-files is compared to the length of a list of files
        generated with the expression glob.glob("<% ctx(fastq_files_path) %>/**/*.fastq.gz", recursive=True)

        - The function should return True, i.e. continue processing without any further
        checks, if the sample sheet is missing lane information.

        - If lane information is detected the expected number of fastq-files
        will be calculated and compared to the list of files. If the expected number of
        files is found the return value is True,
        otherwise false (to enable retry until all expected files are transferred).

        param sample_sheet_file: string
        param file_list: list
        return: boolean
    """

    with open(sample_sheet_file) as file:
        sample_sheet_list = file.readlines()

    if not any(line.startswith("Lane,") for line in sample_sheet_list):
        return True
    else:
        paired_end = False
        nr_of_samples = 0
        lane_count = []
        for line in sample_sheet_list:
            if not line.startswith("Lane,"):
                if re.search("Read2Cycles", line):
                    paired_end = True

            if re.search("^[0-9]+,", line):
                nr_of_samples += 1
                if line.split(",")[0] not in lane_count:
                    lane_count.append(line.split(",")[0])

        expected_undetermined = len(lane_count)
        if paired_end:
            expected_fastqs = 2*(expected_undetermined + nr_of_samples)
        else:
            expected_fastqs = expected_undetermined + nr_of_samples

        if expected_fastqs == len(file_list):
            return True
        else:
            return False
