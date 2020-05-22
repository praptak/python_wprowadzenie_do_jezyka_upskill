from unittest.mock import patch, Mock

import pytest
from click.testing import CliRunner

from lottery.lottery import Lottery
from main import main


def test_main_no_arguments():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 2
    assert result.output == \
           """Usage: main [OPTIONS] PARTICIPANTS
Try \'main --help\' for help.

Error: Missing argument \'PARTICIPANTS\'.
"""


@pytest.mark.parametrize(
    'participants',
    ['participants1', 'participants2', 'wrong_participants3']
)
@patch('lottery.read_data.read_data')
@patch('lottery.filepath.get_lottery_file')
@patch('lottery.filepath.get_participants_file')
@patch('lottery.lottery.Lottery')
@patch.object(Lottery, 'draw')
@patch.object(Lottery, 'show')
def test_main_participants(mock_lottery_show, mock_lottery_draw, mock_lottery, mock_get_participants_file, mock_get_lottery_file, mock_read_data, participants):
    runner = CliRunner()
    result = runner.invoke(main, [participants])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    'participants, option, participants_format',
    [
        ('any', '-f', 'json'),
        ('any', '-f', 'csv'),
        ('any', '-f', None),
        ('any', '--participants_format', 'json'),
        ('any', '--participants_format', 'csv'),
        ('any', '--participants_format', None)
    ]
)
def test_main_participants_format(participants, option, participants_format):
    runner = CliRunner()
    result = runner.invoke(main, [participants, option, participants_format])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    'participants, option, participants_format',
    [
        ('any', '-f', 'not_csv_nor_json'),
        ('any', '--participants_format', 'not_csv_nor_json')
    ]
)
def test_main_participants_bad_format(participants, option, participants_format):
    runner = CliRunner()
    result = runner.invoke(main, [participants, option, participants_format])
    assert result.exit_code == 2
    assert result.output == """Usage: main [OPTIONS] PARTICIPANTS
Try \'main --help\' for help.

Error: Invalid value for \'--participants_format\' / \'-f\': invalid choice: not_csv_nor_json. (choose from json, csv)
"""


@pytest.mark.parametrize(
    'option, lottery',
    [
        ('-l', 'any'),
        ('--lottery_template', 'any')
    ]
)
def test_main_lottery_template(option, lottery):
    runner = CliRunner()
    result = runner.invoke(main, ['participants', option, lottery])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    'option, results_path',
    [
        ('-r', 'any'),
        ('--results_path', 'any')
    ]
)
def test_main_results_path(option, results_path):
    runner = CliRunner()
    result = runner.invoke(main, ['participants', option, results_path])
    assert result.exit_code == 0


def test_main_result_wrong_option():
    runner = CliRunner()
    result = runner.invoke(main, ['participants', '--wrong_argument', 'any_value'])
    assert result.exit_code == 2
    assert result.output == """Usage: main [OPTIONS] PARTICIPANTS
Try \'main --help\' for help.

Error: no such option: --wrong_argument
"""
