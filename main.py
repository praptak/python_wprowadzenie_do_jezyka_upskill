from typing import Dict, List

import click

from lottery.filepath import get_lottery_file, get_participants_file
from lottery.lottery import Lottery, LotteryTemplate
from lottery.participants import create_list_with_weighed_participants
from lottery.read_data import read_data


@click.command()
@click.argument('participants')
@click.option(
    '--participants_format', '-f',
    help=f'Choose participants file data type from list. If not provided, \'json\' type will be chosen.',
    type=click.Choice(['json', 'csv']),
    default='json'
)
@click.option(
    '--lottery_template', '-l',
    help='Choose lottery template from lottery_templates folder. '
         'If not provided, first (in alphabetically order) will be chosen',
    required=False
)
@click.option(
    '--results_path', '-r',
    required=False,
    type=click.Path(exists=False, file_okay=True, writable=True),
    help='To save lottery results, provide path to file. '
         'If not provided, file will not be generated',
    default=None
)
def main(participants, participants_format, lottery_template, results_path) -> None:
    """
    Based on participants data draws alphabetically sorted winners for lottery
    and presents results to screen output and, optionally - to json file
    PARTICIPANTS argument targets filename (without suffix) of file with _participants data.
    """
    try:
        lottery_template_data: Dict = read_data(get_lottery_file(lottery_template).full_path)
        participants_data: List[Dict] = read_data(
            get_participants_file(f'{participants}.{participants_format}').full_path)

        lottery = Lottery(
            LotteryTemplate.from_dict(lottery_template_data),
            create_list_with_weighed_participants(participants_data),
            results_path
        )

        lottery.draw()
        print(lottery.show())
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    main()
