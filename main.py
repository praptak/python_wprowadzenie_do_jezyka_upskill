from typing import Dict, List
import click

# from lottery.filepath import select_participants_file, File
# from lottery.read_data import read_data
# from lottery.lottery import number_of_winners, prize_drawing
from lottery.filepath import get_lottery_file, get_participants_file
from lottery.lottery_functions import create_list_with_weighed_participants
from lottery.prize import LotteryResults, Lottery, LotteryWithParticipants
from lottery.read_data import read_data


def main():
    lottery_with_participants = LotteryWithParticipants.from_dict(
        read_data(get_lottery_file().full_path)
    )

    lottery_with_participants.participants = create_list_with_weighed_participants(
        read_data(get_participants_file('participants1.json').full_path))

    lottery_results = LotteryResults(lottery_with_participants)
    lottery_results.draw_prizes()
    lottery_results.present_results()
    # select file from files folder
    # selected_file: File = select_participants_file()
    #
    # # number of winners
    # winners_number: int = number_of_winners()
    #
    # # read file
    # data: List[Dict] = read_data(selected_file.full_path)
    #
    # # lottery
    # prize_drawing(data, winners_number)
    pass


if __name__ == '__main__':
    main()
