import re


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
                    if 'sample_project' in header_map and columns[header_map['sample_project']].startswith("TM"):
                        data["wp2"]['klinik'].append((columns[header_map['sample_id']], "TM", row))
                    elif 'sample_project' in header_map and columns[header_map['sample_project']].startswith("TE"):
                        data["wp3"]['klinik'].append((columns[header_map['sample_id']], "TE", row))
                    else:
                        if tso500:
                            data["wp1"]['klinik'].append((columns[header_map['sample_id']], "TSO500", row))
                        elif haloplex:
                            data["wp1"]['klinik'].append((columns[header_map['sample_id']], "HaloPlex", row))
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
