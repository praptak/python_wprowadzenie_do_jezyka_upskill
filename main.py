from typing import Dict, List

import click

from lottery.filepath import get_lottery_file, get_participants_file, list_lottery_files
from lottery.lottery import Lottery, LotteryTemplate
from lottery.participants import create_list_with_weighed_participants
from lottery.read_data import read_data


@click.command()
@click.argument('participants')
@click.option('--participants_format', '-f', type=click.Choice(['json', 'csv']), default='json')
@click.option('--lottery_template', '-l', required=False, type=click.Choice([f.name for f in list_lottery_files()]))
@click.option('--results_path', '-r', required=False,
              help='To save lottery results, provide path to file',
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
