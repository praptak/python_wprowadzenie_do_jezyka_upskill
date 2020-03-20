from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


def root():
    return Path(__file__).parent.parent.resolve()


ROOT = root()


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


def list_participants_files() -> List[File]:
    """
    reads data files needed for lottery
    :return: list of File objects for csv and json files within participants folder
    """
    return list_files_in_dir((ROOT / 'files/participants/').resolve(), ['csv', 'json'])


def select_participants_file(file_name: str) -> File:
    """

    :param file_name:
    :return:
    """
    file_list = list_participants_files()

    if not any(file.name.lower() == file_name.lower() for file in file_list):
        raise OSError(2, 'No such file or directory', file_name)

    return next(file for file in file_list if file.name == file_name)

# def select_participants_file() -> File:
#     """
#     prompts user to choose 1 object from list of File objects
#     for participants data, File objects are printed in terminal
#     :return: File object
#     """
#     file_list = list_participants_files()
#     while True:
#         print('Lista plików:')
#         for num, file in enumerate(file_list, 1):
#             print(f'\t{num}: {file.name}')
#
#         try:
#             input_number = int(input('\nWskaż nr pliku z próbą do losowania: '))
#         except ValueError:
#             print('\nWskaż poprawny numer!')
#             continue
#
#         if input_number < 1 or input_number > len(file_list):
#             print('\nWskaż poprawny numer!')
#             continue
#
#         selected_file = file_list[input_number - 1]
#         print(f'Wybrano plik {input_number}: {selected_file}')
#         return selected_file
