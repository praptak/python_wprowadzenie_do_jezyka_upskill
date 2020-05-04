from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from lottery.filepath import get_lottery_file, File, get_participants_file, PARTICIPANTS_FOLDER


@pytest.fixture
def mock_participants_folder(monkeypatch):
    patched = Path('mock_participants_folder')
    monkeypatch.setattr('lottery.filepath.PARTICIPANTS_FOLDER', patched)
    return patched


@pytest.mark.parametrize('test_file_name', ['sdsda'])
def test_get_participants_file(test_file_name, mock_participants_folder):
    test_path = File
    test_path.exists = MagicMock(return_value=True)
    expected = File(test_file_name, mock_participants_folder / test_file_name)
    actual = get_participants_file(test_file_name)
    assert expected.name == actual.name
    assert expected.full_path == actual.full_path


@pytest.mark.parametrize('test_file_name', ['sdsda'])
def test_get_participants_file_exception_raised(test_file_name, mock_participants_folder):
    test_path = File
    test_path.exists = MagicMock(return_value=False)
    with pytest.raises(FileNotFoundError):
        get_participants_file(test_file_name)


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
        get_lottery_file(file_name)
