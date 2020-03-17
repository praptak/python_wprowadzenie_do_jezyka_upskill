import random
from typing import List, Dict

from lottery.participants import ParticipantWeighed


def number_of_winners() -> int:
    """
    prompts user to choose number of winning participants
    number must be a positive integer
    :return: int
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


def create_list_with_weighed_participants(participants_data_list: List[Dict]) -> List[ParticipantWeighed]:
    """
    creates list of ParticipantWeighed objects from dictionary
    :param participants_data_list: List[Dict] - dictionary that contains data about participants
    :return: List[ParticipantWeighed]
    """
    return [ParticipantWeighed(participant_id=record.pop("id"), **record) for record in participants_data_list]


def lottery(weighed_participants_list: List[ParticipantWeighed], num: int) -> List[ParticipantWeighed]:
    """
    draws set of winners from ParticipantWeighed objects list
    :param weighed_participants_list: list of participants with weigh
    :param num: number of winners - size of set
    :return: set of ParticipantWeighed objects - winners of lottery
    """
    if num >= len(weighed_participants_list):
        return weighed_participants_list

    temp_weighed_participants = list(weighed_participants_list)
    results: List[ParticipantWeighed] = list()
    while len(results) < num:
        participant = random.choices(
            population=temp_weighed_participants,
            weights=[int(p.weight) for p in temp_weighed_participants]
        )[0]

        results.append(participant)
        temp_weighed_participants.remove(participant)

    return results


def prize_drawing(data: List[Dict], num: int) -> None:
    """
    calls lottery, sorts and prints it's results
    :param data: dictionary with participants
    :param num: number of winners

    """
    res = sorted(lottery(create_list_with_weighed_participants(data), num))
    print('', 'Wylosowano następujące osoby:', sep='\n')
    for x in res:
        print(f'\t{x}')
