from typing import Dict, List
import click

from lottery.filepath import select_participants_file, File
from lottery.read_data import read_data
from lottery.lottery import number_of_winners, prize_drawing


def main():
    # select file from files folder
    selected_file: File = select_participants_file()

    # number of winners
    winners_number: int = number_of_winners()

    # read file
    data: List[Dict] = read_data(selected_file.full_path)

    # lottery
    prize_drawing(data, winners_number)


if __name__ == '__main__':
    main()
