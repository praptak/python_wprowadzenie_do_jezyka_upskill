import csv
import json


def read_json(path):
    with open(path, 'r') as json_file:
        return json.load(json_file)


def read_csv(path):
    with open(path, 'r') as csv_file:
        records = []
        for row in csv.DictReader(csv_file, skipinitialspace=True):
            records.append(row)
        return records


def read_data(path):
    suffix = str(path).split(".")[-1].lower()
    if suffix == 'csv':
        return read_csv(path)
    elif suffix == 'json':
        return read_json(path)
    else:
        raise TypeError("Wrong file type provided")