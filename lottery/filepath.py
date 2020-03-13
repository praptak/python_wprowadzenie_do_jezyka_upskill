from pathlib import Path
from string import Template


# this is project's root folder - I don't know how to do it better :(
def root():
    return Path(__file__).parent.parent.resolve()


ROOT = root()


def searching_all_files(directory_path, file_types=None, recurse=False):
    if file_types is None:
        file_types = ['*']
    dir_path = Path(directory_path)
    temp_file_pattern = Template('$directory*.$file_type')
    assert (dir_path.is_dir())
    assert all([isinstance(file_type, str) for file_type in file_types])
    file_list = []
    [file_list.extend(dir_path.glob(temp_file_pattern.substitute(directory='**/' * recurse, file_type=file_type))) for
     file_type in file_types]

    result_files = []

    for num, f in enumerate(sorted(file_list), 1):
        result_files.append(MyFile(num, f.resolve().name, f.resolve()))

    return result_files


def list_files_in_files_folder():
    return searching_all_files((ROOT / 'files/participants/').resolve(), ['csv', 'json'])


def select_participants_file():
    file_list = list_files_in_files_folder()
    assert all([isinstance(x, MyFile) for x in file_list])
    selected_file = ""
    while selected_file not in file_list:
        while True:
            print('Lista plików:')
            [print(f'\t{file.id}: {file.name}') for file in file_list]
            print()
            try:
                input_number = int(input('Wskaż nr pliku z próbą do losowania: ')) - 1
                if input_number < 0:
                    continue
                selected_file = file_list[input_number]
                print('Wybrano plik', selected_file, end='\n')
                return selected_file
            except:
                print('Wskaż poprawny numer!')


class MyFile:
    def __init__(self, id, name, fullpath):
        self.id = id
        self.name = name
        self.fullpath = fullpath

    def __repr__(self):
        return f'{self.id}: {self.name}'
