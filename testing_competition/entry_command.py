import glob
import subprocess

from pathlib import Path

import click
from typing import NamedTuple, List, Tuple

from testing_competition.language_identifier import PythonTestIdentifier


class ContributorResult(NamedTuple):
    """
    Summary of contribution of one author
    """
    name: str
    number_of_tests: int
    percentage_of_tests: float


def get_git_blame(path_test):
    pass


def find_test_base_contributors(path_directory: Path) -> Tuple[int, List[ContributorResult]]:
    """
    Given the path to a git repo, compute who wrote most tests
    :param path_directory:
    :return:
    """
    str_path_directory = str(path_directory.absolute())
    python_identifier = PythonTestIdentifier()
    for candidate_path in glob.iglob(str_path_directory + '/**/' + python_identifier.file_glob_pattern(),
                                     recursive=True):
        candidate_path = Path(candidate_path).absolute()
        candidate_filename = candidate_path.name
        if python_identifier.is_a_test_file(candidate_filename):
            p = subprocess.Popen(['git', 'blame', candidate_path],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE
                                 )
            out, err = p.communicate()
            blame_lines = out.splitlines()
            print(blame_lines)

            import sys
            sys.exit(1)


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
