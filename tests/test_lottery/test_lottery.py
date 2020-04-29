import builtins
import random
from pathlib import Path
from unittest.mock import patch, mock_open
import pytest

from lottery.lottery import Lottery, LotteryTemplate, Prize, LotteryResults, PrizeWinners
from lottery.participants import ParticipantWeighed


class TestLottery:

    @pytest.fixture()
    def lottery(self):
        return Lottery(
            LotteryTemplate('lottery', [Prize(1, 'first', 1), Prize(2, 'seconds', 2)]),
            [
                ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5),
                ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4),
                ParticipantWeighed('FirstName_c', 'Lastname_c', 3, 3),
                ParticipantWeighed('FirstName_d', 'Lastname_d', 4, 2),
                ParticipantWeighed('FirstName_e', 'Lastname_e', 5, 1)
            ]
        )

    def test_draw(self, lottery):
        lottery.draw()

    @patch.object(LotteryResults, 'present_results', autospec=True)
    def test_show(self, present_mock, lottery):
        lottery.show()
        present_mock.assert_called_once()


class TestLotteryResults:
    @pytest.fixture()
    def lottery_results(self):
        return LotteryResults(
            'results', [
                PrizeWinners(
                    Prize(1, 'first', 1),
                    [ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)]
                )
            ]
        )

    @patch.object(LotteryResults, '_sort_results', autospec=True)
    @patch.object(LotteryResults, '_show_results', autospec=True)
    @patch.object(builtins, 'open', autospec=True)
    @pytest.mark.parametrize('file_path', [None, Path('file_path')])
    def test_present_results(self, open_mock, show_mock, sort_mock, file_path, lottery_results):
        lottery_results.present_results(file_path)
        show_mock.assert_called_once()
        sort_mock.assert_called_once()
        if file_path is None:
            open_mock.assert_not_called()
        else:
            open_mock.assert_called_once_with(str(file_path), 'w')
