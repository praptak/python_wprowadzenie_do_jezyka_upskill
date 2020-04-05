from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Generator

ROOT = Path(__file__).parent.parent.resolve()
PARTICIPANTS_FOLDER = (ROOT / 'files/participants/').resolve()
LOTTERY_TEMPLATES_FOLDER = (ROOT / 'files/lottery_templates/').resolve()


@dataclass(frozen=True)
class File:
    name: str
    full_path: Path

    def __str__(self):
        return self.name


def list_files_in_dir(
        directory_path: Path,
        file_types: Optional[List[str]] = None,
        recurse: bool = False) -> List[File]:
    """
    lists recursively (if needed) all files within directory, matching file type suffixes
    :param directory_path: path to directory
    :param file_types: list of strings - should contain suffixes for searched files,
    if None, all file types will be listed
    :param recurse: if true, additionally checks all subdirectories recursively,
    if false - reads only root folder (directory_path)
    :return: list of File objects
    """
    if file_types is None:
        file_types = ['*']
    dir_path = Path(directory_path)
    file_list = list()
    for file_type in file_types:
        if recurse:
            temp_file = f'**/*.{file_type}'
        else:
            temp_file = f'*.{file_type}'
        file_list.extend(dir_path.glob(temp_file))

    return [File(f.resolve().name, f.resolve()) for f in sorted(file_list)]


def get_participants_file(file_name: str) -> File:
    """
    searches for file with participants data in participants folder matching it's name with param value provided
    :param file_name: str
    :return: File object matching file_name name
    """

    matching_files_list: List[Path] = list(PARTICIPANTS_FOLDER.glob(file_name))
    if len(matching_files_list) == 0:
        raise FileNotFoundError(f'Participants data file {file_name} not found!')

    matching_file = matching_files_list[0]
    return File(matching_file.resolve().name, matching_file.resolve())


def gen_lottery_files() -> Generator[File, None, None]:
    """
    as generator iterates through files within lottery_templates directory
    :return: yields File
    """

    for file in list_files_in_dir(LOTTERY_TEMPLATES_FOLDER, ['json']):
        yield file


def get_lottery_file(file_name: str = None) -> File:
    """
    searches for file with lottery template data in lottery_templates folder matching it's name with
    param value provided.
    If no file_name param provided, the first file from folder (in alphabetical order) is returned
    :param file_name: str
    :return: File
    """

    if file_name is None:
        return next(gen_lottery_files())
    return next(file for file in gen_lottery_files() if file.name == file_name)
