import types
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from lottery.filepath import get_lottery_file, File, get_participants_file, gen_lottery_files


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


@pytest.mark.parametrize('test_file_name', ['example_file.txt'])
def test_get_participants_file(test_file_name, mock_participants_folder):
    with patch.object(File, 'exists', MagicMock(return_value=True)):
        expected = File(test_file_name, mock_participants_folder / test_file_name)
        actual = get_participants_file(test_file_name)
    assert expected.name == actual.name
    assert expected.full_path == actual.full_path


@pytest.mark.parametrize('test_file_name', ['example_file.txt'])
def test_get_participants_file_exception_raised(test_file_name, mock_participants_folder):
    with patch.object(File, 'exists', MagicMock(return_value=False)):
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
    with patch.object(File,'exists', MagicMock(return_value=exists)):
        with patch('lottery.filepath.gen_lottery_files') as mock:
            mock.return_value = (file for file in files_list)
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
        with pytest.raises(FileNotFoundError) as e:
            get_lottery_file(file_name)


@pytest.fixture(
    params=[
        (
                [
                    'file_a.json',
                    'file_b.other',
                    'file_c.json'
                ],
                [
                    'file_a.json',
                    'file_c.json'
                ]
        ),
        (
                [],
                []
        )
    ]
)
def mock_lottery_templates_folder_gen(tmpdir, monkeypatch, request):
    patched = tmpdir.mkdtemp()
    for record in request.param[0]:
        patched.join(record).write('content')
    monkeypatch.setattr('lottery.filepath.LOTTERY_TEMPLATES_FOLDER', Path(patched.strpath))
    return [File(file_name, Path(patched.strpath) / file_name) for file_name in request.param[1]]


def test_gen_lottery_files(mock_lottery_templates_folder_gen):
    expected_result = mock_lottery_templates_folder_gen
    actual_results = gen_lottery_files()
    assert isinstance(actual_results, types.GeneratorType)
    assert expected_result == list(actual_results)
