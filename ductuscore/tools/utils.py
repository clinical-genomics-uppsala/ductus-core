def parse_sample_sheet(samplesheet):
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
