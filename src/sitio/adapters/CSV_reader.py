import csv

def parse_csv2(fnm):
    from sitio.common.utils import num
    csv_reader = csv.reader(open(fnm,'rU'), delimiter=';', quotechar='"')
    data = {}
    csv_reader.next() # skip the header
    for row in csv_reader:
        if len(row) > 2:
            data[row[0]] = map(num, row[1:])
        else:
            data[row[0]] = num(row[1])
    return data

def parse_csv3(fnm):
    csv_reader = csv.reader(open(fnm,'rU'), delimiter=',', quotechar='\'')
    data = []
    csv_reader.next() # skip the header
    for row in csv_reader:
        data.append(row)
    return data