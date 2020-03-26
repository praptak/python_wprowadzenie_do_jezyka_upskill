import errno
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


def root() -> Path:
    return Path(__file__).parent.parent.resolve()


ROOT = root()


def get_participants_folder() -> Path:
    return (ROOT / 'files/participants/').resolve()


def get_lottery_templates_folder() -> Path:
    return (ROOT / 'files/lottery_templates/').resolve()


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

    matching_files_list: List[Path] = list(get_participants_folder().glob(file_name))
    if len(matching_files_list) == 0:
        print(f'Participants data file {file_name} not found!')
        sys.exit(errno.ENODATA)

    matching_file = matching_files_list[0]
    return File(matching_file.resolve().name, matching_file.resolve())


def list_participants_files() -> List[File]:
    """
    returns data files needed for lottery from participants folder
    :return: List[File]
    """

    return list_files_in_dir(get_participants_folder())


def get_lottery_file(file_name: str = None) -> File:
    """
    searches for file with lottery template data in lottery_templates folder matching it's name with
    param value provided.
    If no file_name param provided, the first file from folder (in alphabetical order) is returned
    :param file_name: str
    :return: File
    """

    lottery_files_list: List[File] = list_lottery_files()
    if file_name is None:
        return lottery_files_list[0]
    try:
        return next(file for file in lottery_files_list if file.name == file_name)
    except StopIteration:
        print(f'Lottery template data file {file_name} not found!')
        sys.exit(errno.ENODATA)


def list_lottery_files() -> List[File]:
    """
    presents list of file within lottery_templates directory
    :return: List[File]
    """

    return list_files_in_dir(get_lottery_templates_folder(), ['json'])
