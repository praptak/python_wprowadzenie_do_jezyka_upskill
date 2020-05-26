import csv
import json
from pathlib import Path
from typing import Dict, List, Union


def read_json(path: str) -> Union[List[Dict], Dict]:
    """
    converts json file to list of dictionaries
    :param path: absolute path to file
    :return: List[Dict]
    """
    with open(path, 'r') as json_file:
        return json.load(json_file)


def read_csv(path: str) -> List[Dict]:
    """
   converts csv file to list of dictionaries
   :param path: absolute path to file
   :return: List[Dict]
   """
    with open(path, 'r') as csv_file:
        return list(csv.DictReader(csv_file, skipinitialspace=True))


def read_data(path: Path) -> Union[List[Dict], Dict]:
    """
    converts data from file to list of dictionaries depending on file type
    if file type is not csv nor json, a TypeError is raised
    :param path: absolute path to file
    :return: List[Dict]
    """
    suffix = path.suffix.lower()
    if suffix == '.csv':
        return read_csv(str(path))
    elif suffix == '.json':
        return read_json(str(path))
    else:
        raise TypeError('Wrong file type provided')
