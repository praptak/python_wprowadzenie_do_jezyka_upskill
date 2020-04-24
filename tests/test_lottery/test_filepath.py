from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from lottery.filepath import get_lottery_file, File, get_participants_file, PARTICIPANTS_FOLDER


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


@pytest.fixture()
def gen_lottery_files_mock():
    def file_generator():
        for file in [File('file_a', Path('dir_a/file_a')), File('file_b', Path('dir_b/file_b'))]:
            yield file

    return file_generator()


@pytest.fixture()
def empty_gen_lottery_files_mock():
    def file_generator():
        yield from ()

    return file_generator()


@pytest.mark.parametrize('file_name, exists', [(None, True), ('file_b', True)])
# @pytest.mark.parametrize('exists', [True, True])
def test_get_lottery_file(gen_lottery_files_mock, file_name, exists):
    with patch('lottery.filepath.gen_lottery_files') as mock:
        Path.exists = MagicMock(return_value=exists)
        mock.return_value = gen_lottery_files_mock
        assert get_lottery_file(file_name)


@pytest.mark.parametrize('file_name', [None, 'file_c'])
@patch('lottery.filepath.gen_lottery_files')
@patch('pathlib.Path.exists')
def test_get_lottery_file_raise_exception(
        mock_exists,
        mock_gen_lottery_files,
        empty_gen_lottery_files_mock,
        file_name):
    mock_exists.return_value = False
    mock_gen_lottery_files.return_value = empty_gen_lottery_files_mock
    with pytest.raises(FileNotFoundError) as e:
        assert get_lottery_file(file_name)
