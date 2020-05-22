import builtins
from pathlib import Path
from unittest.mock import patch, mock_open
import pytest

from lottery.lottery import Lottery, LotteryTemplate, Prize, LotteryResults, PrizeWinners
from lottery.participants import ParticipantWeighed


class TestLottery:
    @pytest.fixture()
    def lottery_mock(self):
        return Lottery(
            LotteryTemplate('lottery', [Prize(1, 'First', 1), Prize(2, 'second', 2)]),
            [
                ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5),
                ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4),
                ParticipantWeighed('FirstName_c', 'Lastname_c', 3, 3),
                ParticipantWeighed('FirstName_d', 'Lastname_d', 4, 2),
                ParticipantWeighed('FirstName_e', 'Lastname_e', 5, 1)
            ]
        )

    @pytest.mark.parametrize(
        'lottery_template_name, lottery_template_prizes, participants, random_choices, expected_results',
        [
            (
                    'lottery_data_single_winner_five_weighed_participants',
                    [Prize(1, 'first', 1)],
                    [
                        ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5),
                        ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4),
                        ParticipantWeighed('FirstName_c', 'Lastname_c', 3, 3),
                        ParticipantWeighed('FirstName_d', 'Lastname_d', 4, 2),
                        ParticipantWeighed('FirstName_e', 'Lastname_e', 5, 1)
                    ],
                    [
                        [ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)]
                    ],
                    LotteryResults('lottery_data_single_winner_five_weighed_participants', [
                        PrizeWinners(Prize(1, 'first', 1), [ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)])])
            ),
            (
                    'lottery_data_two_lotteries_first_single_second_2_giveaway_prizes_five_weighed_participants',
                    [Prize(1, 'first', 1), Prize(2, 'second', 2)],
                    [
                        ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5),
                        ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4),
                        ParticipantWeighed('FirstName_c', 'Lastname_c', 3, 3),
                        ParticipantWeighed('FirstName_d', 'Lastname_d', 4, 2),
                        ParticipantWeighed('FirstName_e', 'Lastname_e', 5, 1)
                    ],
                    [
                        [ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)],
                        [ParticipantWeighed('FirstName_e', 'Lastname_e', 5, 1)],
                        [ParticipantWeighed('FirstName_c', 'Lastname_c', 3, 3)]

                    ],
                    LotteryResults(
                        'lottery_data_two_lotteries_first_single_second_2_giveaway_prizes_five_weighed_participants',
                        [
                            PrizeWinners(Prize(1, 'first', 1), [ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)]),
                            PrizeWinners(
                                Prize(2, 'second', 2),
                                [
                                    ParticipantWeighed('FirstName_e', 'Lastname_e', 5, 1),
                                    ParticipantWeighed('FirstName_c', 'Lastname_c', 3, 3)
                                ]
                            )
                        ]
                    )
            ),
            (
                    'lottery_data_single_2_giveaway_prizes_zero_weighed_participants',
                    [Prize(1, 'first', 1)],
                    [],
                    [['does not matter']],
                    LotteryResults(
                        'lottery_data_single_2_giveaway_prizes_zero_weighed_participants',
                        [
                            PrizeWinners(Prize(1, 'first', 1), [])
                        ]
                    )
            ),
            (
                    'lottery_data_two_lotteries_first_single_second_2_giveaway_prizes_2_weighed_participants',
                    [Prize(1, 'first', 1), Prize(2, 'second', 2)],
                    [
                        ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5),
                        ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4)
                    ],
                    [
                        [ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)],
                        [ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4)],
                        ['does not matter']

                    ],
                    LotteryResults(
                        'lottery_data_two_lotteries_first_single_second_2_giveaway_prizes_2_weighed_participants',
                        [
                            PrizeWinners(Prize(1, 'first', 1), [ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)]),
                            PrizeWinners(
                                Prize(2, 'second', 2),
                                [
                                    ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4)
                                ]
                            )
                        ]
                    )
            )
        ]
    )
    def test_draw(self, lottery_template_name, lottery_template_prizes, participants, expected_results, random_choices):
        lottery = Lottery(LotteryTemplate(lottery_template_name, lottery_template_prizes), participants)
        with patch('random.choices', side_effect=random_choices):
            lottery.draw()

        assert lottery._lottery_results == expected_results

    @patch.object(LotteryResults, 'present_results', autospec=True)
    def test_show(self, present_mock, lottery_mock):
        lottery_mock.show()
        present_mock.assert_called_once()


class TestLotteryResults:
    @pytest.fixture()
    def mock_lottery_results_single(self):
        return LotteryResults(
            'results', [
                PrizeWinners(
                    Prize(1, 'first', 1),
                    [ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)]
                )
            ]
        )

    @pytest.fixture()
    def mock_lottery_results_single_show(self):
        return f'Lottery: results\n\tWinner(s) of "first" prize:\n\t\tFirstName_a Lastname_a'

    @pytest.fixture()
    def lottery_results_many(self):
        return LotteryResults(
            'lottery_results_many',
            [
                PrizeWinners(
                    Prize(1, 'first', 2),
                    [
                        ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4),
                        ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)
                    ]
                ),
                PrizeWinners(
                    Prize(2, 'second', 2),
                    [
                        ParticipantWeighed('FirstName_e', 'Lastname_e', 5, 1),
                        ParticipantWeighed('FirstName_c', 'Lastname_c', 3, 3)
                    ]
                )
            ]
        )

    @pytest.fixture()
    def lottery_results_many_sorted(self):
        return LotteryResults(
            'lottery_results_many',
            [
                PrizeWinners(
                    Prize(1, 'first', 2),
                    [
                        ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5),
                        ParticipantWeighed('FirstName_b', 'Lastname_b', 2, 4)
                    ]
                ),
                PrizeWinners(
                    Prize(2, 'second', 2),
                    [
                        ParticipantWeighed('FirstName_c', 'Lastname_c', 3, 3),
                        ParticipantWeighed('FirstName_e', 'Lastname_e', 5, 1)
                    ]
                )
            ]
        )

    @pytest.fixture()
    def lottery_results_many_sorted_show(self):
        return f'Lottery: lottery_results_many\n\tWinner(s) of "first" prize:\n\t\tFirstName_a Lastname_a\n\t\tFirstName_b Lastname_b\n\tWinner(s) of "second" prize:\n\t\tFirstName_c Lastname_c\n\t\tFirstName_e Lastname_e'

    @pytest.fixture()
    def lottery_results_empty(self):
        return LotteryResults('empty', [])

    @pytest.fixture()
    def lottery_results_empty_show(self):
        return 'Lottery: empty'

    @pytest.fixture(params=[
        ('mock_lottery_results_single', 'mock_lottery_results_single'),
        ('lottery_results_many', 'lottery_results_many_sorted'),
        ('lottery_results_empty', 'lottery_results_empty')
    ]
    )
    def mock_lottery_results(
            self,
            request
    ):
        return (
            request.getfixturevalue(request.param[0]),
            request.getfixturevalue(request.param[1])
        )

    @pytest.fixture(params=[
        ('lottery_results_empty', 'lottery_results_empty_show'),
        ('mock_lottery_results_single', 'mock_lottery_results_single_show'),
        ('lottery_results_many_sorted', 'lottery_results_many_sorted_show')
    ]
    )
    def mock_lottery_results_show(self, request):
        return (
            request.getfixturevalue(request.param[0]),
            request.getfixturevalue(request.param[1])
        )

    @patch.object(LotteryResults, '_sort_results', autospec=True)
    @patch.object(LotteryResults, '_show_results', autospec=True)
    @patch.object(builtins, 'open', autospec=True)
    @pytest.mark.parametrize('file_path', [None, Path('file_path')])
    def test_present_results(self, open_mock, show_mock, sort_mock, file_path, mock_lottery_results_single):
        mock_lottery_results_single.present_results(file_path)
        show_mock.assert_called_once()
        sort_mock.assert_called_once()
        if file_path is None:
            open_mock.assert_not_called()
        else:
            open_mock.assert_called_once_with(str(file_path), 'w')

    def test_show_results(self, mock_lottery_results_show):
        lottery_results = mock_lottery_results_show[0]
        expected_output = mock_lottery_results_show[1]
        actual_output = lottery_results._show_results()
        assert expected_output == actual_output

    @pytest.mark.parametrize('data_to_write', ['supercalifragilisticexpialidoucious'])
    def test_save_results(self, data_to_write):
        file_path = 'file_path.txt'
        lottery_results = LotteryResults('lottery_name', [])
        open_mock = mock_open()
        with patch('json.dumps', return_value=data_to_write):
            with patch('builtins.open', open_mock):
                lottery_results._save_results(Path(file_path))

        open_mock.assert_called_with(file_path, "w")
        open_mock.return_value.write.assert_called_once_with(data_to_write)

    def test_sort_results(self, mock_lottery_results):
        lottery_results = mock_lottery_results[0]
        expected_results = mock_lottery_results[1]
        lottery_results._sort_results()
        assert lottery_results == expected_results
