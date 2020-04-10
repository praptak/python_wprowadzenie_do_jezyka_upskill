from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Generator

ROOT = Path(__file__).parent.parent
PARTICIPANTS_FOLDER = (ROOT / 'files/participants/')
LOTTERY_TEMPLATES_FOLDER = (ROOT / 'files/lottery_templates/')


@dataclass(frozen=True)
class File:
    name: str
    full_path: Path

    def __str__(self):
        return self.name

    def exists(self):
        return self.full_path.exists()


def get_participants_file(file_name: str) -> File:
    """
    searches for file with participants data in participants folder matching it's name with param value provided
    :param file_name: str
    :return: File object matching file_name name
    """

    file: File = File(file_name, PARTICIPANTS_FOLDER / file_name)

    if not file.exists():
        raise FileNotFoundError(f'Participants data file {file_name} not found!')

    return file


def gen_lottery_files() -> Generator[File, None, None]:
    """
    as generator iterates through files within lottery_templates directory
    :return: yields File
    """

    for f in sorted(LOTTERY_TEMPLATES_FOLDER.glob('*.json')):
        yield File(f.resolve().name, f.resolve())


def get_lottery_file(file_name: str = None) -> File:
    """
    searches for file with lottery template data in lottery_templates folder matching it's name with
    param value provided.
    If no file_name param provided, the first file from folder (in alphabetical order) is returned
    :param file_name: str
    :return: File
    """
    try:
        if file_name is None:
            return next(gen_lottery_files())
    except StopIteration:
        raise FileNotFoundError(f'No files found in {LOTTERY_TEMPLATES_FOLDER.name}')

    file: File = File(file_name, LOTTERY_TEMPLATES_FOLDER / file_name)
    if not file.exists():
        raise FileNotFoundError(f'File {file} does not exist!')
    return file
