import json, csv
from pathlib import Path
from unittest.mock import patch, mock_open
from io import StringIO
import pytest

from lottery.read_data import read_data, read_json, read_csv


@pytest.fixture()
def csv_data_mock():
    new_csvfile = StringIO()
    data = [{'a': 1, 'b': 2, 'c': 3}, {'a': 2, 'b': 3, 'c': 4}]
    wr = csv.writer(new_csvfile)
    wr = csv.DictWriter(new_csvfile, fieldnames=data[0].keys())

    for row in data:
        wr.writerow(row)
        # for key in row.keys():
        #     wr.writerow(row[key])
    
    return new_csvfile


@patch('builtins.open', mock_open(read_data=json.dumps({'a': 1, 'b': 2, 'c': 3})), create=True)
@pytest.mark.parametrize('test_file_name', ['sdsda'])
def test_read_json(test_file_name):
    assert read_json(test_file_name)


# @patch('builtins.open', mock_open(read_data=str(StringIO("""\
# col1,col2,col3
# 1,3,foo
# 2,5,bar
# -1,7,baz"""))), create=True)


@pytest.mark.parametrize('path', [Path('dir_a/file_a.csv'), Path('dir_a/file_b.json')])
@patch('lottery.read_data.read_json')
@patch('lottery.read_data.read_csv')
def test_read_data(mock_read_csv, mock_read_json, path):
    assert read_data(path)


@pytest.mark.parametrize('path', [Path('dir_a/file_a.other_file_type')])
@patch('lottery.read_data.read_json')
@patch('lottery.read_data.read_csv')
def test_read_data_raise_exception(mock_read_csv, mock_read_json, path):
    with pytest.raises(TypeError) as e:
        assert read_data(path)


@pytest.mark.parametrize('test_file_name', ['sdsda'])
@patch('builtins.open')
def test_read_csv(open_mock, test_file_name, csv_data_mock):
    open_mock.mock_open(read_data=csv_data_mock)
    open_mock.create = True
    with open_mock:
        assert read_csv(test_file_name)
