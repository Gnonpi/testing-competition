import glob
import re
import subprocess
from pathlib import Path
from typing import Tuple, List

from testing_competition.custom_types import ContributorResult, BlameLine
from testing_competition.language_identifier import PythonTestIdentifier

RE_PARSE_BLAME = re.compile(r'(?P<commit_hash>.+) \((?P<commit_author>[\w0-1]+)\s{1,}(?P<commit_date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \+0200\s*(?P<line_number>\d+)\)(?P<content>.*)')
NOT_COMMITTED_MSG = 'Not Committed Yet'

def get_git_blame(path_test: Path) -> List[BlameLine]:
    p = subprocess.Popen(['git', 'blame', path_test],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE
                         )
    out, err = p.communicate()
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
    str_path_directory = str(path_directory.absolute())
    python_identifier = PythonTestIdentifier()
    for candidate_path in glob.iglob(str_path_directory + '/**/' + python_identifier.file_glob_pattern(),
                                     recursive=True):
        candidate_path = Path(candidate_path).absolute()
        candidate_filename = candidate_path.name
        if python_identifier.is_a_test_file(candidate_filename):
            blame_lines = get_git_blame(candidate_path)
            print(blame_lines)
            python_identifier.extract_test_functions(blame_lines)

            import sys
            sys.exit(1)
