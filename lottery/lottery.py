import json
import random
from dataclasses import dataclass, asdict
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

        self._sort_results()

        if file_path is not None:
            self._save_results(file_path)

        return self._show_results()

    def _show_results(self) -> str:
        """
        iterates through each lottery prizes results and returns all prizes and prize winners
        :return: str_results
        """
        str_results = f'Lottery: {self.lottery_name}'
        for res in self.results:
            str_results += f'\n\tWinner(s) of {res.prize}:'
            for winner in res.winners:
                str_results += f'\n\t\t{winner}'

        return str_results

    def _save_results(self, file_path: Path) -> None:
        """
        saves lottery results into json file
        :param file_path: where to save data
        :return:
        """
        json_str = json.dumps(asdict(self), indent=2, sort_keys=True)
        with open(str(file_path), 'w') as file:
            file.write(json_str)

    def _sort_results(self) -> None:
        """
        sorts list of winners for each prize
        :return:
        """
        for result in self.results:
            result.winners.sort()


class Lottery:
    def __init__(self, lottery_template: LotteryTemplate, participants: List[ParticipantWeighed],
                 save_path: Optional[Path] = None):
        self._lottery_template = lottery_template
        self._participants = participants
        self._save_path = save_path
        self._remaining_participants = self._participants
        self._lottery_results = LotteryResults(self._lottery_template.name, list())

    def draw(self) -> None:
        """
        iterates through lottery prizes collection in _lottery_template.
        draws list of winners for each list of prize in collection depending on available amount of prize
        during the lottery process, __remaining_participants list is used. If _participants wins a prize, he/she will be
        removed from __remaining_participants. The list is used for further lottery process until all winners are drown


        :return:
        """
        for prize in self._lottery_template.prizes:
            prize_winners = PrizeWinners(prize, list())

            while len(prize_winners.winners) < prize_winners.prize.amount:
                if prize_winners.prize.amount >= len(self._remaining_participants):
                    prize_winners.winners.extend(self._remaining_participants)
                    self._remaining_participants.clear()
                    break

                participant: ParticipantWeighed = random.choices(
                    population=self._remaining_participants,
                    weights=[p.weight for p in self._remaining_participants]
                )[0]

                self._remaining_participants.remove(participant)
                prize_winners.winners.append(participant)

            self._lottery_results.results.append(prize_winners)

    def show(self) -> str:
        """
        returns lottery results as string and optionally to json file
        results will be saved in json format only if _save_path field targets the file
        all lists of winners for each prize is sorted alphabetically
        :return: str - formatted multi-line string with lottery results
        """
        return self._lottery_results.present_results(self._save_path)
