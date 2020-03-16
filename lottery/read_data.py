import csv
import json
from pathlib import Path


def read_json(path):
    """
    converts json file to list of dictionaries
    :param path: absolute path to file
    :return: List[Dict]
    """
    with open(path, 'r') as json_file:
        return json.load(json_file)


def read_csv(path):
    """
   converts csv file to list of dictionaries
   :param path: absolute path to file
   :return: List[Dict]
   """
    with open(path, 'r') as csv_file:
        return [row for row in csv.DictReader(csv_file, skipinitialspace=True)]


def read_data(path: Path):
    """
    converts data from file to list of dictionaries depending on file type
    if file type is not csv nor json, a TypeError is raised
    :param path: absolute path to file
    :return: List[Dict]
    """
    # suffix = str(path).split('.')[-1].lower()
    suffix = path.suffix.lower()
    if suffix == '.csv':
        return read_csv(path)
    elif suffix == '.json':
        return read_json(path)
    else:
        raise TypeError('Wrong file type provided')
