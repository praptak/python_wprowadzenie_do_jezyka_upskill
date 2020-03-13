from lottery.filepath import select_participants_file
from lottery.read_data import read_data
from lottery.lottery import number_of_winners, prize_drawing


def main():
    # select file from files folder
    selected_file = select_participants_file()

    # number of winners
    winners_number = number_of_winners()

    # read file
    data = read_data(selected_file.fullpath)

    # lottery
    prize_drawing(data, winners_number)


if __name__ == '__main__':
    main()
