from src.modules.filepath import select_file
from src.modules.read_data import read_data
from src.modules.lottery import number_of_winners, prize_drawing

# select file from files folder
selected_file = select_file()

# number of winners
winners_number = number_of_winners()

# read file
data = read_data(selected_file.fullpath)

# lottery
prize_drawing(data, winners_number)
