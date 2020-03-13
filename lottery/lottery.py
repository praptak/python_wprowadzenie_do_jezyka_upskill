import random
from typing import List, Dict

from lottery.participants import ParticipantWeighed, Participant


# how many winners in the lottery
def number_of_winners():
    """

    :return:
    """
    while True:
        try:
            winners_number = int(input('Podaj liczbę uczestników do wylosowania: '))
        except ValueError:
            print('Podaj poprawny numer!')
            continue

        if winners_number <= 0:
            print('Numer musi być dodatni!')
            continue

        return winners_number


# list with weighed participants ###
def create_list_with_weighed_participants(participants_data_list: List[Dict]):
    """

    :param participants_data_list:
    :return:
    """
    return [ParticipantWeighed(**record) for record in participants_data_list]


# trial list based on weigh ####
def create_trial_list(weighed_participants_list: List[ParticipantWeighed]):
    """

    :param weighed_participants_list:
    :return:
    """
    return [Participant(record.id, record.first_name, record.last_name) for record in
            weighed_participants_list for _ in
            range(int(record.weight))]


# set of winners drawn from list, based on given number
def lottery(participants_list: List[Participant], num: int):
    """

    :param participants_list:
    :param num:
    :return:
    """
    results = set()
    # to avoid edge cases
    if num >= len(set(participants_list)):
        return set(participants_list)

    temp_sample_list = list(participants_list)

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
    """

    :param data:
    :param num:
    :return:
    """
    res = sorted(lottery(create_trial_list(create_list_with_weighed_participants(data)), num))
    print('', 'Wylosowano następujące osoby:', sep='\n')
    for x in res:
        print(f'\t{x}')
