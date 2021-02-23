import re


def contains(workpackage, analysis, samnplesheet):
    data = extract_analysis_information(samnplesheet)
    if workpackage in data:
        for type, analyzes in data[workpackage].items():
            for a_item in analyzes:
                if analysis in a_item:
                    return True
    return False


def get_samples_and_project(workpackage, analysis, samnplesheet):
    data = extract_analysis_information(samnplesheet)
    sample_project = []
    if workpackage in data:
        for project_type, data in data[workpackage].items():
            for d in data:
                if analysis in d:
                    sample_project.append((d[0], project_type))
    return sample_project


def get_project_types(workpackage, analysis, samnplesheet):
    data = extract_analysis_information(samnplesheet)
    project_types = []
    if workpackage in data:
        for project_type, analyzes in data[workpackage].items():
            for a_item in analyzes:
                if analysis in a_item:
                    project_types.append(project_type)
    return set(project_types)


def print_project_types(workpackage, analysis, samnplesheet):
    print(*get_project_types(workpackage, analysis, samnplesheet), sep="\n")


def extract_analysis_information(samplesheet):
    """
        Function used to extract samples from a SampleSheet.csv and group them after
        workpackage and project type, example Klinik,s
    """
    with open(samplesheet) as file:
        haloplex = False
        tso500 = False
        TM = False
        TE = False
        data = {'header': "",
                'wp1': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []},
                'wp2': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []},
                'wp3': {'klinik': [], 'projekt': [], 'forskning': [], 'utveckling': []}}
        for line in file:
            data['header'] = data['header'] + line
            line = line.lower()
            if "haloplex" in line:
                haloplex = True
            if "pooldna" in line or "poolrna" in line:
                tso500 = True
            if "name,te" in line:
                TE = True
            if "name,tm" in line:
                TM = True
            if line.startswith("[data]"):
                line = next(file)
                data['header'] = data['header'] + line
                header_map = {v[1].lower(): v[0] for v in enumerate(re.split(",|;", line.rstrip()))}
                for row in file:
                    columns = re.split(",|;", row)
                    if len(columns) == 1:
                        continue
                    if 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("tm"):
                        data["wp2"]['klinik'].append((columns[header_map['sample_id']], "tm", row))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].lower().startswith("te"):
                        data["wp3"]['klinik'].append((columns[header_map['sample_id']], "te", row))
                    else:
                        if tso500:
                            data["wp1"]['klinik'].append((columns[header_map['sample_id']], "tso500", row))
                        elif haloplex:
                            data["wp1"]['klinik'].append((columns[header_map['sample_id']], "sera", row))
                        else:
                            raise Exception("Unhandled case: " + row)
        return data


def extract_wp_and_typo(samplesheet):
    """
        Function used to extract samples from a SampleSheet.csv and group them after
        workpackage and project type, example Klinik,s
    """
    with open(samplesheet) as file:
        haloplex = False
        tso500 = False
        TM = False
        TE = False
        for line in file:
            if("HaloPlex" in line):
                haloplex = True
            if("PoolDNA" in line or "PoolRNA" in line):
                tso500 = True
            if("Name,TE" in line):
                TE = True
            if("Name,TM" in line):
                TM = True
            if line.startswith("[Data]"):
                break
        return (('haloplex', haloplex), ('tso500', tso500), ('te', TE), ('tm', TM))
