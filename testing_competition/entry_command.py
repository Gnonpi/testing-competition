import logging
from pathlib import Path

import click
from typing import List

from testing_competition.analyse_repo import find_test_base_contributors
from testing_competition.custom_types import ContributorResult

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('testing_competition')


def print_contributor_results(total_tests: int, contributor_list: List[ContributorResult]):
    """
    Pretty print the contributors contributions
    :param total_tests:
    :param contributor_list:
    :return:
    """
    pass


@click.command()
@click.argument('directory', type=click.Path(exists=True))
def main_command(directory):
    """
    Main entrypoint for the package
    :param directory:
    :return:
    """
    path_directory = Path(directory).resolve()
    if not path_directory.exists():
        raise FileNotFoundError(f'Could not find directory {path_directory}')
    total_test, contributor_list = find_test_base_contributors(path_directory)
    print_contributor_results(total_test, contributor_list)


if __name__ == '__main__':
    main_command()
