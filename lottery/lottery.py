import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from lottery.participants import ParticipantWeighed


@dataclass(frozen=True, eq=True, repr=True, order=True)
class Prize:
    id: int
    name: str
    amount: int

    def __str__(self):
        return f'"{self.name}" prize'


@dataclass(frozen=True, eq=True, repr=False, order=True)
class LotteryTemplate:
    name: str
    prizes: List[Prize]

    @classmethod
    def from_dict(cls, a_dict):
        return cls(a_dict['name'], [Prize(**record) for record in a_dict['prizes']])


@dataclass(frozen=False, eq=True, repr=True, order=True)
class PrizeWinners:
    prize: Prize
    winners: List[ParticipantWeighed]


@dataclass(frozen=False, eq=True, repr=True, order=True)
class LotteryResults:
    lottery_name: str
    results: List[PrizeWinners]

    def present_results(self, file_path: Optional[Path] = None) -> str:
        """
        calls show_results method to list winners for each lottery reward
        if file_path parameter is given, it save the results into external file with given path
        :param file_path: path to save data
        :return: lottery results from __show_results method
        """

        if file_path is not None:
            self.__save_results(file_path)

        return self.__show_results()

    def __show_results(self) -> str:
        """
        iterates through each lottery prizes results and returns all prizes and prize winners
        :return: str_results
        """
        str_results = f'Lottery: {self.lottery_name}'
        for res in self.results:
            str_results += f'\n\tWinner(s) of {res.prize}:'
            for winner in sorted(res.winners):
                str_results += f'\n\t\t{winner}'

        return str_results

    def __save_results(self, file_path: Path) -> None:
        """
        saves lottery results into json file
        :param file_path: where to save data
        :return:
        """
        json_str = json.dumps(self, default=lambda o: o.__dict__, indent=2)
        with open(str(file_path), 'w') as file:
            file.write(json_str)


@dataclass(frozen=False, eq=True, repr=False, order=True)
class Lottery(object):
    lottery_template: LotteryTemplate
    participants: List[ParticipantWeighed]
    save_path: Optional[Path] = None
    __lottery_results: LotteryResults = field(init=False)
    __remaining_participants: List[ParticipantWeighed] = field(init=False)

    def __post_init__(self):
        self.__remaining_participants = self.participants
        self.__lottery_results = LotteryResults(self.lottery_template.name, list())

    def __lottery(self):
        """

        :return:
        """
        for prize in self.lottery_template.prizes:
            prize_winners = PrizeWinners(prize, list())

            while len(prize_winners.winners) < prize_winners.prize.amount:
                if prize_winners.prize.amount >= len(self.__remaining_participants):
                    prize_winners.winners.extend(self.__remaining_participants)
                    self.__remaining_participants.clear()
                    break

                participant: ParticipantWeighed = random.choices(
                    population=self.__remaining_participants,
                    weights=[int(p.weight) for p in self.__remaining_participants]
                )[0]

                self.__remaining_participants.remove(participant)
                prize_winners.winners.append(participant)

            self.__lottery_results.results.append(prize_winners)

    def draw(self) -> None:
        """
        calls lottery depending on participants list and lottery_template
        :return:
        """
        self.__lottery()

    def show(self) -> str:
        """
        returns lottery results as string and optionally to json file
        :return:
        """
        return self.__lottery_results.present_results(self.save_path)
