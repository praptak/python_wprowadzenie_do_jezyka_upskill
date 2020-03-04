import random
from src.Data.participants import ParticipantWeighed, Participant


#### create list with weighed participants ###
def create_list_with_weighed_participants(list):
    weighed_list = []
    for record in list:
        weighed_list.append(ParticipantWeighed.from_dict(record))

    return weighed_list


#### create trial list based on weigh ####
def create_trial_list(list):
    trial_list = []
    for record in list:
        for weigh in range(int(record.weight)):
            trial_list.append(Participant(record.id, record.first_name, record.last_name))

    return trial_list


def lottery(participants_list, num):
    results = set()
    # to avoid edge cases
    if num >= len(set(participants_list)):
        return set(participants_list)

    while len(results) < num:
        random_number = random.randrange(0, len(participants_list))
        results.add(participants_list[random_number])

    return results


def number_of_winners():
    while True:
        try:
            winners_number = int(input("Podaj liczbę uczestników do wylosowania: "))
            if winners_number <= 0:
                print("Numer musi być dodatni!")
                continue
            return winners_number
        except:
            print("Podaj poprawny numer!")
