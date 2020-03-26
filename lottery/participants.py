from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True, eq=True, repr=False, order=True)
class Participant:
    first_name: str
    last_name: str
    participant_id: int

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return self.full_name()


@dataclass(frozen=True, eq=True, repr=False, order=True)
class ParticipantWeighed(Participant):
    weight: int = 1


def create_list_with_weighed_participants(participants_data_list: List[Dict]) -> List[ParticipantWeighed]:
    """
    creates list of ParticipantWeighed objects from dictionary
    :param participants_data_list: List[Dict] - dictionary that contains data about participants
    :return: List[ParticipantWeighed]
    """
    return [ParticipantWeighed(participant_id=int(record.pop("id")), weight=int(record.pop("weight", 1)), **record) for
            record
            in participants_data_list]
