import pytest

from unittest.mock import MagicMock, patch
from pathlib import Path

from lottery.filepath import PARTICIPANTS_FOLDER, get_participants_file, get_lottery_file, File


@pytest.mark.parametrize('test_file_name', ['sdsda'])
def test_get_participants_file(test_file_name):
    test_participants_folder = PARTICIPANTS_FOLDER
    file = File(test_file_name, test_participants_folder / test_file_name)
    test_path = Path
    test_path.exists = MagicMock(return_value=True)
    assert get_participants_file(test_file_name) == file


def test_get_participants_file_exception_raised():
    test_file_name = 'test_file_name'
    test_path = Path
    test_path.exists = MagicMock(return_value=False)
    with pytest.raises(FileNotFoundError):
        assert get_participants_file(test_file_name)


def test_gen_lottery_files():
    pass


@pytest.fixture
def gen_lottery_files_mock():
    return [File('file_a', Path('dir_a/file_a')), File('file_b', Path('dir_b/file_b'))]


def test_get_lottery_file(gen_lottery_files_mock):
    with patch('lottery.filepath.gen_lottery_files') as mock:
        mock.return_value = gen_lottery_files_mock
        get_lottery_file('file_a')
