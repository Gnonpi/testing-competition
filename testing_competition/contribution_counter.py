import logging
from collections import defaultdict
from typing import List

from testing_competition.custom_types import FunctionTest, ContributorResult


class ContributionCounter:
    """
    Class to keep track of the edits made in tests
    """
    def __init__(self):
        self.map_contributor_results = dict()
        self.total_number_tests = 0
        self.total_number_lines = 0

    def update_contributions(self, list_tests: List[FunctionTest]):
        """
        Given a list of test contents update the stats of the contributors
        :param list_tests:
        :return:
        """
        logger = logging.getLogger('testing_competition')
        logger.info('Updating contributions')

        for function_test in list_tests:
            logger.debug(f'Counting for {function_test.name_test}')
            lines_per_author = defaultdict(int)

            for line in function_test.list_lines:
                line_author = line.author
                if line_author not in self.map_contributor_results:
                    self.map_contributor_results[line_author] = ContributorResult(name=line_author)
                lines_per_author[line_author] += 1
            highest_participation = 0
            owner_of_test = None

            for author, lines_added in lines_per_author.items():
                self.map_contributor_results[author].number_of_lines_written += lines_added
                self.map_contributor_results[author].number_of_tests_associated += 1
                if lines_added > highest_participation:
                    highest_participation = lines_added
                    owner_of_test = author

            self.total_number_tests += 1
            self.total_number_lines += len(function_test.list_lines)
            self.map_contributor_results[owner_of_test].number_of_tests_owned += 1

    def update_percentages(self):
        """
        Update the stats of contributors with current totals of tests and lines
        :return:
        """
        logger = logging.getLogger('testing_competition')
        logger.info('Updating contribution percentages')
        for author, contributor in self.map_contributor_results.items():
            perc_tests_owned = self.map_contributor_results[author].number_of_tests_owned / self.total_number_tests
            perc_tests_associated = self.map_contributor_results[author].number_of_tests_associated / self.total_number_tests
            perc_lines_written = self.map_contributor_results[author].number_of_lines_written / self.total_number_lines
            self.map_contributor_results[author].percentage_of_tests_owned = perc_tests_owned * 100
            self.map_contributor_results[author].percentage_of_tests_associated = perc_tests_associated * 100
            self.map_contributor_results[author].percentage_of_lines_written = perc_lines_written * 100