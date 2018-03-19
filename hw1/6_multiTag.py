
#!/usr/bin/python3
import re
def readfile(file):
    return open(file, "r")


#Following function adds type RARE and other 3 new classes to contain different low-frequency words.
def replacewords(f_count, f_raw, f_write):
    b = readfile(f_count)
    record = {}
    for line in b:
        if "WORDTAG" in line:
            item = line.split(" ")
            if item[-1].strip("\n") in record:
                record[item[-1].strip("\n")] += int(item[0])
            else:
                record[item[-1].strip("\n")] = int(item[0])
    for key in record.copy():
        if record[key]>=5:
            del record[key]

    raw = readfile(f_raw)
    regex = r"\b[A-Z][a-zA-Z\.]*[A-Z]\b\.?"
    pat = r"\b[0-9\.\-\"\'\,\?]*\b"
    with open(f_write, 'w+') as f:
        for row in raw:
            segments = row.split(" ")
            if segments[0] in record:
                if segments[0] in re.findall(pat, segments[0]):
                    segments[0] = "_Numeric_"
                elif segments[0].isupper():
                    segments[0] = "_All-Capitals_"
                elif segments[0] in re.findall(regex, segments[0]):
                    segments[0] = "_Acronyms_"
                else:
                    segments[0] = "_RARE_"    
            f.write(" ".join(segments))

def run():
    replacewords('ner.counts','ner_train.dat','ner_train_multiTag.dat')

run()

