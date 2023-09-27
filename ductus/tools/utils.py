from collections.abc import Mapping
import datetime
import re
from copy import deepcopy


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
                        print(d)
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


def get_experiments(samplesheet):
    data = extract_analysis_information(samplesheet)
    del data['header']
    experiments = {}
    print(data)
    for wp in data:
        for type in data[wp]:
            for item in data[wp][type]:
                if item and item[1] in experiments:
                    if experiments[item[1]]['analysis'] == item[3] and experiments[item[1]]['wp'] == wp:
                        experiments[item[1]]['samples'].append(item[0])
                    else:
                        raise Exception(f"Trying to mix different wp or analyis within the same experiment. Experiment "
                                        "{item[1]}, adding ({wp}, {item[3]}) to f{experiments[item[1]]})")
                else:
                    experiments[item[1]] = {'analysis': item[3], 'wp': wp, 'samples': [item[0]]}
    return experiments


def extract_analysis_information(samplesheet):
    """
        Function used to extract samples from a SampleSheet.csv and group them after
        workpackage and project type, example Klinik,s
    """
    with open(samplesheet) as file:
        pattern = re.compile(r"experiment name,\d{8}_[a-z0-9-]+")
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
                'wp3': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []}}
        date_string = datetime.date.today().strftime("%Y%m%d")

        file_format_version = "v1"
        for line in file:
            if "FileFormatVersion,2" in line:
                file_format_version = "v2"
            if line.startswith("Date"):
                if "/" in line:
                    date_result = re.search(r"Date,(\d{1,2})/(\d{1,2})/(\d{4})", line)
                    date_string = "{}{:02d}{:02d}".format(date_result[3], int(date_result[1]), int(date_result[2]))
                else:
                    date_result = re.search(r"^Date,(\d{4})-{0,1}(\d{1,2})-{0,1}(\d{1,2})", line)
                    date_string = "{}{:02d}{:02d}".format(date_result[1], int(date_result[2]), int(date_result[3]))
            if file_format_version == "v1" and line.lower().startswith("[data]"):
                data = parse_v1_format(file, data, date_string)
            elif file_format_version == "v2" and line.lower().startswith("[bclconvert_settings]"):
                data = parse_v2_format("bclconvert", file, data, date_string)
            else:
                data['header'] = data['header'] + line
        return data


def parse_v1_format(file_iterator, data, date):
    line = next(file_iterator)
    header_map = {v[1].lower(): v[0] for v in enumerate(re.split(",|;", line.rstrip()))}

    sample_name_key = "sample_id"
    project_key = "sample_project"
    description_key = "description"

    for key in header_map:
        if "project" in key:
            project_key = key

    for row in file_iterator:
        columns = re.split(",|;", row.rstrip())

        if len(columns) <= 1:
            continue
        (wp, analysis, experiment) = columns[header_map[project_key]].rstrip().split("_")
        data[wp.lower()]['klinik'].append((columns[header_map[sample_name_key]],
                                           experiment, date,
                                           analysis.lower(),
                                           columns[header_map[description_key]],
                                           row))
    return data


def parse_v2_format(application, file_iterator, data, date):
    application_data = {}
    sample_name_key = "sample_id"
    project_key = "sample_project"
    description_key = "description"

    def merge_application_data(data):
        def merge(dict1, dict2):
            result = deepcopy(dict1)
            for key, value in dict2.items():
                if isinstance(value, Mapping):
                    result[key] = merge(result.get(key, {}), value)
                elif isinstance(value, list):
                    result[key] = result[key] + value
                else:
                    result[key] = deepcopy(dict2[key])
            return result
        keys = [k for k in data.keys()]
        temp = data[keys[0]]
        for key in keys[1:]:
            temp = merge(temp, data[key])
        return temp

    def parse_section(application, application_data, file_iterator, date):
        application_data[application] = {'wp1': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []},
                                         'wp2': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []},
                                         'wp3': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []}}
        for row in file_iterator:
            application_search = re.search(r"\[([A-Za-z0-9-])+_data\]", row.lower())
            if application_search:
                row = next(file_iterator)
                header_map = {v[1].lower(): v[0] for v in enumerate(re.split(",|;", row.rstrip()))}
                for row in file_iterator:
                    application_search = re.search(r'([A-Za-z0-9-])+_settings', row.lower())
                    if not application_search:
                        columns = re.split(",|;", row.rstrip())
                        if len(columns) <= 1 or application == "bclconvert":
                            continue
                        (wp, analysis, experiment) = columns[header_map[project_key]].split("_")
                        application_data[application][wp.lower()]['klinik'].append((columns[header_map[sample_name_key]],
                                                                                    experiment, date,
                                                                                    analysis,
                                                                                    columns[header_map[description_key]],
                                                                                    row))
                    else:
                        application_data = parse_section(application_search.group(0), application_data, file_iterator, date)
        return application_data

    parse_section(application, application_data, file_iterator, date)
    del application_data['bclconvert']
    application_data = merge_application_data(application_data)

    return {**data, **application_data}
