import datetime
import json
import os
import re


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


def is_old_ductus_format(samplesheet, new_format_regex=["20[0-9]{6}-[-A-Z]*-[0-9]*-[0-9]*",
                                                        "BCRABL[0-9]*-[A-Z]{1}[0-9-]*",
                                                        "TE[0-9]*-[A-Z0-9-]*",
                                                        "TM[0-9]*-[A-Z0-9-]*",
                                                        "TC[0-9]*-[A-Z0-9-]*"]):
    new_format = False
    s_data = extract_analysis_information(samplesheet)
    for wp in s_data:
        if wp.startswith("wp"):
            for project_type, data in s_data[wp].items():
                for d in data:
                    if True in {re.match(r, d[0]) is not None for r in new_format_regex}:
                        new_format = True
    return not new_format

def convert_old_cgu_samplesheet_format_to_new(samplesheet, new_file):
    with open(new_file, "w") as writer:
        s_data = extract_analysis_information(samplesheet)
        writer.write(s_data['header'])
        for wp in s_data:
            if wp.startswith("wp"):
                for _, data in s_data[wp].items():
                    for d in data:
                        new_samplesheet_format = f"{d[1]}-{d[0]}".replace('_', '-')
                        writer.write(d[-1].replace(d[0], new_samplesheet_format))

def create_analysis_file(samplesheet, outputfolder):
    def create_description(wp, data):
        if "wp1" == wp:
            if re.match(r"[10]+\.[0-9]+", data):
                return f"TC:{data}" 
            else:
                return ""
        elif wp in ["wp2", "wp3"]:
            keys = ['panel', 'gender', 'trio', 'experiment', 'project']
            return "_".join(map(lambda v: f"{v[0]}:{v[1]}", zip(keys, data.split('_'))))
        elif "wp3":
            return "wp3"
    s_data = extract_analysis_information(samplesheet)
    files_created = []
    for wp in s_data:
        if wp.startswith("wp"):
            for _, data in s_data[wp].items():
                if data:
                    files_created.append(os.path.join(outputfolder, f"{data[0][1]}_analysis.csv"))
                    with open(files_created[-1], 'w') as writer:
                        writer.write(",".join(["Workpackage", "Experiment", "Analysis", "Sample_ID", "Description"]))
                        for d in data:
                            writer.write('\n' + ','.join([
                                wp,
                                d[1].replace('_', '-'),
                                d[3],
                                d[0],
                                create_description(wp, d[4])
                        ]))
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
                        user = d[1].split("_")[1]
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
                'wp3': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []}}
        date_string = None
        experiment = None
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
                experiment = re.search("^Experiment Name,([A-Za-z0-9_-]+)", line)[1]
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
                    if 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("tm"):
                        data["wp2"]['klinik'].append((columns[header_map['sample_name']],
                                                      experiment, date_string,
                                                      "tm",
                                                      description,
                                                      row))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("abl"):
                        data["wp2"]['klinik'].append((columns[header_map['sample_name']],
                                                      experiment, date_string,
                                                      "abl",
                                                      description,
                                                      row))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("te"):
                        data["wp3"]['klinik'].append((columns[header_map['sample_name']],
                                                      experiment,
                                                      date_string,
                                                      "te",
                                                      description,
                                                      row))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("tc"):
                        data["wp3"]['klinik'].append((columns[header_map['sample_name']],
                                                      experiment,
                                                      date_string,
                                                      "tc",
                                                      description,
                                                      row))
                    else:
                        if tso500:
                            data["wp1"]['klinik'].append((columns[header_map['sample_id']],
                                                          experiment,
                                                          date_string,
                                                          "tso500",
                                                          description,
                                                          row))
                        elif sera:
                            data["wp1"]['klinik'].append((columns[header_map['sample_name']],
                                                          experiment,
                                                          date_string,
                                                          "sera",
                                                          description,
                                                          row))
                        elif gms560:
                            data["wp1"]['klinik'].append((columns[header_map['sample_id']],
                                                          experiment,
                                                          date_string,
                                                          "gms560",
                                                          description,
                                                          row))
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
