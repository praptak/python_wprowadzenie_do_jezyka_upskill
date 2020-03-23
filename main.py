from typing import Dict, List

import click

from lottery.filepath import get_lottery_file, get_participants_file
from lottery.lottery import Lottery, LotteryTemplate
from lottery.participants import create_list_with_weighed_participants
from lottery.read_data import read_data


@click.command()
@click.argument('participants')
@click.option('--participants_format', '-f', default='json',
              type=click.Choice(['json', 'csv'], case_sensitive=False),
              show_default=True, show_choices=True)
@click.option('--lottery_template', type=(str, int), default=0)
@click.option('--results_path', required=False,
              help='To save lottery results, provide path to file',
              resolve_path=True,
              default=None)
def main(participants, participants_format, lottery_template, results_path):
    lottery_template_data: Dict = read_data(get_lottery_file(lottery_template).full_path)
    participants_data: List[Dict] = read_data(get_participants_file(f'{participants}.{participants_format}').full_path)

    lottery = Lottery(
        LotteryTemplate.from_dict(lottery_template_data),
        create_list_with_weighed_participants(participants_data),
        results_path
    )

    lottery.draw()
    print(lottery.show())


if __name__ == '__main__':
    main()
