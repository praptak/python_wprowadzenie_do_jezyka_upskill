from pathlib import Path


def root():
    return Path(__file__).parent.parent.parent.resolve()


ROOT = root()


def searching_all_files(directory, lst):
    dirpath = Path(directory)
    assert (dirpath.is_dir())
    assert all([isinstance(x, str) for x in lst])
    file_list = []
    [file_list.extend(dirpath.glob(f"**/*.{suffix}")) for suffix in lst]
    lottery_files_list = []

    for num, f in enumerate(file_list, 1):
        lottery_files_list.append(LotteryFile(num, f.resolve().name, f.resolve()))

    return lottery_files_list


def list_files_in_files_folder():
    return searching_all_files((ROOT / "files/").resolve(), ['csv', 'json'])


def select_file():
    lottery_file_list = list_files_in_files_folder()
    selected_file = ""
    while selected_file not in lottery_file_list:
        while True:
            print("Lista plików:")
            [print(f"\t{x.id}: {x.name}") for x in lottery_file_list]
            print()
            try:
                input_number = int(input("Wskaż nr pliku z próbą do losowania: ")) - 1
                if input_number < 0:
                    continue
                selected_file = lottery_file_list[input_number]
                print("Wybrano plik", selected_file, end="\n")
                return selected_file
            except:
                print("Wskaż poprawny numer!")


class LotteryFile:
    def __init__(self, id, name, fullpath):
        self.id = id
        self.name = name
        self.fullpath = fullpath

    def __repr__(self):
        return f"{self.id}: {self.name}"
