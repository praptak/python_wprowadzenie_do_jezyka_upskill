import json, csv
from pathlib import Path
from textwrap import dedent
from unittest.mock import patch, mock_open
from io import StringIO
import pytest

from lottery.read_data import read_data, read_json, read_csv


@patch('builtins.open', mock_open(read_data=json.dumps({'a': 1, 'b': 2, 'c': 3})), create=True)
@pytest.mark.parametrize('test_file_name', ['sdsda'])
def test_read_json(test_file_name):
    assert read_json(test_file_name)


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
def test_read_csv(open_mock, test_file_name):
    read_csv(test_file_name)
    open_mock.assert_called_once_with(test_file_name, 'r')
