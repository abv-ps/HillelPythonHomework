import csv, re


class Delimiter(csv.Dialect):
    delimiter = ';'
    quotechar = '"'
    lineterminator = '\n'
    quoting = csv.QUOTE_ALL


csv.register_dialect('delimiter', Delimiter)

with open('data.csv', encoding= 'utf-8') as csvfile:
    data = csvfile.read()
    print(re.sub(r'(?<=\d),(?=\d)', ';', data))




