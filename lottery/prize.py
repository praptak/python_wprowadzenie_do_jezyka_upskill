import json
from dataclasses import dataclass, field
from pathlib import Path
import random
from typing import List, Optional, Dict

from lottery.participants import ParticipantWeighed


@dataclass(frozen=True, eq=True, repr=False, order=True)
class Prize:
    id: int
    name: str
    amount: int

    def __repr__(self):
        return f'Reward: {self.name}'


@dataclass(frozen=False, eq=True, repr=False, order=True)
class Lottery:
    name: str
    prizes: List[Prize]

    def __repr__(self):
        return f'Lottery name: {self.name}'

    @classmethod
    def from_dict(cls, a_dict):
        return cls(a_dict['name'], [Prize(**record) for record in a_dict['prizes']])


@dataclass(frozen=False, eq=True, repr=False, order=True)
class LotteryWithParticipants(Lottery):
    participants: Optional[List[ParticipantWeighed]] = None


@dataclass(frozen=False, eq=True, repr=False, order=True)
class Winner:
    participant: ParticipantWeighed
    prize: Prize

    def __str__(self):
        return f'{self.participant} wins {self.prize} prize.'


@dataclass(frozen=False, eq=True, repr=False, order=True)
class LotteryResults:
    lottery: LotteryWithParticipants
    winners: Optional[List[Winner]] = field(default_factory=list)
    json_file: Optional[Path] = None
    __ongoing_participants: Optional[List[ParticipantWeighed]] = None

    def __print_results(self) -> None:
        print(f'Results of lottery: {self.lottery}:')
        for winner in sorted(self.winners):
            print(f'\t{winner}')

    def __save_to_file(self) -> None:
        if len(str(self.json_file)) == 0:
            return

        with open(str(self.json_file), 'w') as file:
            file.write(json.dumps(self.__dict__, indent=2))

    def __lottery(self, prize: Prize) -> None:
        """
        draws set of winners from ParticipantWeighed objects list
        :param prize:
        :param weighed_participants_list: list of participants with weigh
        :param num: number of winners - size of set
        :return: set of ParticipantWeighed objects - winners of lottery
        """

        self.__ongoing_participants = [participant for participant in self.lottery.participants if
                                       participant not in self.winners]

        if prize.amount >= len(self.__ongoing_participants):
            self.winners.extend([Winner(participant, prize) for participant in self.lottery.participants])

        results: List[Winner] = list()
        while len(results) < prize.amount:
            participant = random.choices(
                population=self.__ongoing_participants,
                weights=[int(p.weight) for p in self.__ongoing_participants]
            )[0]

            results.append(Winner(participant, prize))
            self.__ongoing_participants.remove(participant)

        self.winners.extend(results)

    def draw_prizes(self):
        for prize in self.lottery.prizes:
            self.__lottery(prize)

    def present_results(self):
        self.__print_results()
        self.__save_to_file()
