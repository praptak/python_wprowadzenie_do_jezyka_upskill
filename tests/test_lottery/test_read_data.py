import json
from pathlib import Path
from unittest.mock import patch, mock_open
import pytest

from lottery.read_data import read_data, read_json, read_csv


@pytest.mark.parametrize(
    'test_file_path, data',
    [
        ('file_flat', '{"a": 1, "b": 2, "c": 3}'),
        ('file_nested', '{"name":"John","age":30,"cars":{"car1":"Ford","car2":"BMW","car3":"Fiat"}}')
    ]
)
def test_read_json(test_file_path, data):
    with patch('builtins.open', mock_open(read_data=data), create=True) as mock:
        mock.text = data
        actual = read_json(test_file_path)
        expected = json.loads(data)
        assert actual == expected


@pytest.mark.parametrize('path',
                         [Path('dir_a/file_a.csv'), Path('dir_a/file_b.json'), Path('dir_a/file_a.other_file_type')])
@patch('lottery.read_data.read_json')
@patch('lottery.read_data.read_csv')
def test_read_data(mock_read_csv, mock_read_json, path):
    suffix = path.suffix.lower()
    if suffix == '.csv':
        read_data(path)
        mock_read_csv.assert_called_once_with(str(path))
        mock_read_json.assert_not_called()
    elif suffix == '.json':
        read_data(path)
        mock_read_json.assert_called_once_with(str(path))
        mock_read_csv.assert_not_called()
    else:
        with pytest.raises(TypeError):
            read_data(path)


@pytest.fixture()
def csv_expected_output_data():
    return [
        {'col1': '1', 'col2': '3', 'col3': 'foo'},
        {'col1': '2', 'col2': '5', 'col3': 'bar'},
        {'col1': '-1', 'col2': '7', 'col3': 'baz'}
    ]


@pytest.fixture()
def csv_input_data():
    data = """col1,col2,col3
1,3,foo
2,5,bar
-1,7,baz"""
    return data


def test_read_csv(csv_expected_output_data, csv_input_data):
    with patch('builtins.open', mock_open(read_data=csv_input_data), create=True) as mock:
        mock.text = csv_input_data
        actual = read_csv('test_file_path')
        expected = csv_expected_output_data
        assert actual == expected
