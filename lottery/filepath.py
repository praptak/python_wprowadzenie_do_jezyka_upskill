from dataclasses import dataclass
from pathlib import Path
from string import Template

# this is project's root folder - I don't know how to do it better :(
from typing import List


def root():
    return Path(__file__).parent.parent.resolve()


ROOT = root()


def searching_all_files(directory_path: Path, file_types: List[str] = None, recurse: bool = False):
    """

    :param directory_path:
    :param file_types:
    :param recurse:
    :return:
    """
    if file_types is None:
        file_types = ['*']
    dir_path = Path(directory_path)
    file_list: List[File] = []
    for file_type in file_types:
        if recurse:
            temp_file = f'**/*.{file_type}'
        else:
            temp_file = f'*.{file_type}'
        file_list.extend(dir_path.glob(temp_file))

    # return [File(num, f.resolve().name, f.resolve()) for num, f in enumerate(sorted(file_list), 1)]
    return [File(f.resolve().name, f.resolve()) for f in sorted(file_list)]


def list_files_in_files_folder():
    """

    :return:
    """
    return searching_all_files((ROOT / 'files/participants/').resolve(), ['csv', 'json'])


def select_participants_file():
    """

    :return:
    """
    file_list = list_files_in_files_folder()
    while True:
        print('Lista plików:')
        for num, file in enumerate(file_list, 1):
            print(f'\t{num}: {file.name}')

        try:
            input_number = int(input('\nWskaż nr pliku z próbą do losowania: ')) - 1
        except ValueError:
            print('\nWskaż poprawny numer!')
            continue

        if input_number < 0 or input_number > len(file_list) - 1:
            print('\nWskaż poprawny numer!')
            continue

        selected_file = file_list[input_number]
        print(f'Wybrano plik {input_number + 1}: {selected_file}')
        return selected_file


@dataclass(frozen=True)
class File:
    name: str
    full_path: str

    def __repr__(self):
        return self.name
