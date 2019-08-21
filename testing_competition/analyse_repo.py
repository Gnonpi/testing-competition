import glob
import logging
import re
import subprocess
from pathlib import Path
from typing import Tuple, List

from testing_competition.contribution_counter import ContributionCounter
from testing_competition.custom_types import ContributorResult, BlameLine
from testing_competition.language_identifier import PythonTestIdentifier

RE_PARSE_BLAME = re.compile(r'(?P<commit_hash>.+) \((?P<commit_author>[^\s]+)\s{1,}(?P<commit_date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \+0200\s*(?P<line_number>\d+)\)(?P<content>.*)')
NOT_COMMITTED_MSG = 'Not Committed Yet'


def get_git_blame(path_test: Path) -> List[BlameLine]:
    """
    Use git blame on a file to see who edited it via BlameLine
    :param path_test:
    :return:
    """
    p = subprocess.Popen(['git', 'blame', path_test],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE
                         )
    out, err = p.communicate()
    print(out)
    print(err)
    raw_blame_lines = out.splitlines()
    blame_lines = []
    for raw_blame in raw_blame_lines:
        raw_blame = raw_blame.decode('utf8')
        if NOT_COMMITTED_MSG in raw_blame:
            continue
        match_blame = RE_PARSE_BLAME.match(raw_blame)
        if match_blame is None:
            raise RuntimeError('Could not parse line: ' + raw_blame)
        match_blame = match_blame.groupdict()
        blame_lines.append(BlameLine(
            match_blame['commit_hash'],
            match_blame['commit_author'],
            match_blame['commit_date'],
            int(match_blame['line_number']),
            match_blame['content']
        ))
    return blame_lines


def find_test_base_contributors(path_directory: Path) -> Tuple[int, List[ContributorResult]]:
    """
    Given the path to a git repo, compute who wrote most tests
    :param path_directory:
    :return:
    """
    logger = logging.getLogger('testing_competition')
    logger.info(f'Starting to look for tests at: {path_directory}')
    str_path_directory = str(path_directory.absolute())
    contribution_counter = ContributionCounter()
    python_identifier = PythonTestIdentifier()
    for candidate_path in glob.iglob(str_path_directory + '/**/' + python_identifier.file_glob_pattern(),
                                     recursive=True):
        # logger.debug(f"Considering '{candidate_path}'")
        candidate_path = Path(candidate_path).absolute()
        candidate_filename = candidate_path.name
        if python_identifier.is_a_test_file(candidate_filename):
            logger.info(f'Extracting test data from {candidate_filename}')
            blame_lines = get_git_blame(candidate_path)
            list_tests = python_identifier.extract_test_functions(blame_lines)
            print(f'tests: {len(list_tests)}')
            contribution_counter.update_contributions(list_tests)

    contribution_counter.update_percentages()
    for author, contrib in contribution_counter.map_contributor_results.items():
        print(contrib)

    import sys
    sys.exit(1)
