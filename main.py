from src.Data.filepath import select_file
from src.Data.read_data import read_data
from src.Data.lottery import lottery, create_list_with_weighed_participants, create_trial_list, number_of_winners

# select file from files folder
selected_file = select_file()

# number of winners
winners_number = number_of_winners()

# read file
data = read_data(selected_file.fullpath)

# lottery
res = sorted(lottery(create_trial_list(create_list_with_weighed_participants(data)), winners_number))
print("Wylosowano następujące osoby:")
[print(f"\t{x}") for x in res]
