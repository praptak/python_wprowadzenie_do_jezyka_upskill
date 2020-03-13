import random
from lottery.participants import ParticipantWeighed, Participant


# how many winners in the lottery
def number_of_winners():
    while True:
        try:
            winners_number = int(input('Podaj liczbę uczestników do wylosowania: '))
            if winners_number <= 0:
                print('Numer musi być dodatni!')
                continue
            return winners_number
        except:
            print('Podaj poprawny numer!')


# list with weighed participants ###
def create_list_with_weighed_participants(list):
    weighed_list = []
    for record in list:
        weighed_list.append(ParticipantWeighed.from_dict(record))

    return weighed_list


# trial list based on weigh ####
def create_trial_list(list):
    trial_list = []
    for record in list:
        for weigh in range(int(record.weight)):
            trial_list.append(Participant(record.id, record.first_name, record.last_name))

    return trial_list


# set of winners drawn from list, based on given number
def lottery(participants_list, num):
    results = set()
    # to avoid edge cases
    if num >= len(set(participants_list)):
        return set(participants_list)

    temp_sample_list = []

    temp_sample_list.extend(participants_list)

    while len(results) < num:
        random_number = random.randrange(0, len(temp_sample_list))
        # find participant
        participant = temp_sample_list[random_number]
        # add participant to results
        results.add(participant)
        # filter off all participants matching participant from sample list
        temp_sample_list = [x for x in temp_sample_list if x != participant]

    return results


# making a lottery!
def prize_drawing(data, num):
    res = sorted(lottery(create_trial_list(create_list_with_weighed_participants(data)), num))
    print('', 'Wylosowano następujące osoby:', sep='\n')
    [print(f'\t{x}') for x in res]
