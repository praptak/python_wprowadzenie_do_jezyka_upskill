from pathlib import Path


def searching_all_files(directory, lst, num=0):
    dirpath = Path(directory)
    assert (dirpath.is_dir())
    assert all([isinstance(x, str) for x in lst])
    file_list = []
    for x in dirpath.iterdir():
        if x.is_file() and x.name.split(".")[-1] in lst:
            num += 1
            file_list.append(LotteryFile(num, x.resolve().name, x.resolve()))
        elif x.is_dir():
            file_list.extend(searching_all_files(x, lst, num))

    return file_list


def list_files_in_files_folder():
    return searching_all_files((Path(__file__).parent.parent.parent / "files/").resolve(), ['csv', 'json'])


def select_file():
    lottery_file_list = list_files_in_files_folder()
    selected_file = ""
    while selected_file not in lottery_file_list:
        while True:
            [print(x.id, ":", x.name) for x in lottery_file_list]
            try:
                input_number = int(input("Wskaż nr pliku z próbą do losowania: ")) - 1
                if input_number < 0:
                    continue
                selected_file = lottery_file_list[input_number]
                print("Wybrano plik numer: ", selected_file.id)
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
