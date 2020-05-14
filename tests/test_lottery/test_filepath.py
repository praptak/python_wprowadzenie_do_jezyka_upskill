from pathlib import Path
from typing import List, Generator
from unittest.mock import patch, MagicMock
import pytest

from lottery.filepath import get_lottery_file, File, get_participants_file, PARTICIPANTS_FOLDER


@pytest.fixture
def mock_participants_folder(monkeypatch):
    patched = Path('mock_participants_folder')
    monkeypatch.setattr('lottery.filepath.PARTICIPANTS_FOLDER', patched)
    return patched


@pytest.fixture
def mock_lottery_templates_folder(monkeypatch):
    patched = Path('dir')
    monkeypatch.setattr('lottery.filepath.LOTTERY_TEMPLATES_FOLDER', patched)
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


@pytest.mark.parametrize(
    'file_name, exists, return_file, files_list',
    [
        (
                None,
                True,
                File('file_a', Path('dir/file_a')),
                [File('file_a', Path('dir/file_a')), File('file_b', Path('dir/file_b'))]
        ),
        (
                'file_b',
                True,
                File('file_b', Path('dir/file_b')),
                [File('file_a', Path('dir/file_a')), File('file_b', Path('dir/file_b'))]
        )
    ]
)
def test_get_lottery_file(file_name, exists, return_file, mock_lottery_templates_folder,
                          files_list):
    with patch('lottery.filepath.gen_lottery_files') as mock:
        mock.return_value = (file for file in files_list)
        File.exists = MagicMock(return_value=exists)
        expected = return_file
        actual = get_lottery_file(file_name)
        assert expected == actual


@pytest.mark.parametrize(
    'file_name, files_list',
    [
        (None, []),
        ('file_c', [File('file_a', Path('dir/file_a')), File('file_b', Path('dir/file_b'))])
    ]
)
@patch('lottery.filepath.File.exists')
def test_get_lottery_file_raise_exception(
        mock_exists,
        mock_lottery_templates_folder,
        file_name,
        files_list
):
    with patch('lottery.filepath.gen_lottery_files') as mock:
        mock.return_value = (file for file in files_list)
        mock_exists.return_value = False
        # mock_gen_lottery_files.return_value = empty_gen_lottery_files_mock
        with pytest.raises(FileNotFoundError) as e:
            get_lottery_file(file_name)


def test_gen_lottery_files():
    # TODO
    pass
