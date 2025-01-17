"""
Testcases for CorrectBot
TODO Not yet fully functional
"""
import unittest
import sys
sys.path.append('../')  # TODO import that without the dirty hack
from correct_bot import ReducedPage, Corrector
from typing import Dict, Optional, List, Union

def create_reduced_page(language: str, input: List) -> ReducedPage:
    pass

def execute_test(language: str, input_to_test: List[str], expectation: str) -> None:
    """
    Execute the comparison test if input to test will be processed in the way that it matches with the given
    expectation.

    Args:
        language (str): language of the page. Use "__" as placeholder if language is not imporant. 
        input_to_test (List[str]): List of inputs to test the unit on
        expectation (str): Expected output.
    """
    input_to_test: ReducedPage = create_reduced_page(language, input_to_test)
    expected_outcome: ReducedPage = create_reduced_page(language, [expectation])
    # create corrector in fixture, e.g. with https://pythontesting.net/framework/unittest/unittest-fixtures/
    # run correction and ckeck correction with "self.assertEqual(s.split(), ['hello', 'world'])"


class CorrectBotLanguageIndependent(unittest.TestCase):
        # TODO: clarify if we want any uniform rule on the special character "…" versus "..."
        def test_multiple_spaces(self):
            execute_test("__", ["Multiple  whitespaces   test"], "Multiple whitespaces test")

        def test_missing_spaces(self):
            execute_test("__", ["Full stop.Continue,with spaces.Okay?"], "Full stop. Continue, with spaces. Okay?")

        def test_correct_dash(self):
            execute_test("__", ["We don't want this - do we?"], "We don’t want this – do we?")

        def test_file_name(self):
            # TODO real life example of correcting file name reference, see below
            execute_test("__", "Translations:Bible Reading Hints (Seven Stories full of Hope)/6/ml", 62256, 62281)


class CorrectBotRTL(unittest.TestCase):
    """ Test the common rules for right-to-left languages"""
    def test_file_name(self):
        # Check that we're correctly adding a RTL mark when there are parenthesis in file name
        execute_test("__", "Translations:Bible_Reading_Hints_(Seven_Stories_full_of_Hope)/2/fa", 22794, 22801)

    def test_title(self):
        # Check that we're correctly adding a RTL mark when title ends with closing paranthesis: )
        execute_test("__", "Translations:Bible_Reading_Hints_(Seven_Stories_full_of_Hope)/Page_display_title/fa", 57796, 62364)


class CorrectBotEnglish(unittest.TestCase):
    def test_fix_apostrophe(self):
        execute_test("en", ["God's"], "God’s")

    def test_fix_quotation_marks(self):
        execute_test("en", ["\"foo\"", "„foo“"], "“foo”")



class CorrectBotGerman(unittest.TestCase):
    def test_fix_quotation_marks(self):
        # Verify replacement of non-german quotations marks
        execute_test("de", ["“foo”", "\"foo\""], "„foo“")
        # Verify that german quotation marks are used in a correct way ('„' starts and '“' ends a quotation)
        execute_test("de", ["“foo„", "„foo„", "“foo“"], "„foo“")


class CorrectBotFrench(unittest.TestCase):
    def test_false_friends_replacement(self):
        execute_test("fr", ["example"], "exemple")

    def test_ellipsis_fix(self):
        execute_test("fr", ["…"], "...")

    def test_quotation_marks_fix(self):
        # Verify replacement of non-french quotation marks 
        execute_test("fr", ["“foo”", "\"foo\""], "«\u00a0foo\u00a0»")
        # Verify that french quotation marks are used correctly
        execute_test("fr", ["« foo »", "«foo»"], "«\u00a0foo\u00a0»")


class CorrectBotSpain(unittest.TestCase):
    def test_fix_ellipsis(self):
        execute_test("es", ["…"], "...")


class CorrectBotArabic(unittest.TestCase):
    def test_fix_comma(self):
        execute_test("ar", [","], "،")
        execute_test("ar", ["منهم،حتى"], "منهم، حتى")

    def test_fix_multiple_spaces(self):
        test_removal_double_whitespaces: List(str) = ["يدعي  و يصلي"]
        expectation_double_whitespaces: str = "يدعي و يصلي"
        execute_test("ar", test_removal_double_whitespaces, expectation_double_whitespaces)

        test_removal_whitespaces_before_comma: List(str) = ["بحرص ،  أن"]
        expectation_whitespaces_before_comma: str = "بحرص، أن"
        execute_test("ar", test_removal_whitespaces_before_comma, expectation_whitespaces_before_comma)

    def test_real_life_examples(self):
        # TODO can we have an option to read real translations from the system and compares them?
        # Liking checking that correctbot would correct in the same way as it was done here manually:
        # something like execute_test(language_code: str, translation_unit: str, revision_id_before, revision_id_after)
        # See these API calls for the first line:
        # https://www.4training.net/mediawiki/index.php?title=Translations:How_to_Continue_After_a_Prayer_Time/1/ar&action=history
        # https://www.4training.net/mediawiki/index.php?title=Translations:How_to_Continue_After_a_Prayer_Time/1/ar&oldid=62195
        # https://www.4training.net/mediawiki/index.php?title=Translations:How_to_Continue_After_a_Prayer_Time/1/ar&oldid=62258
        execute_test("ar", "Translations:How_to_Continue_After_a_Prayer_Time/1/ar", 62195, 62258)
        execute_test("ar", "Translations:How to Continue After a Prayer Time/4/ar", 62201, 62260)
        execute_test("ar", "Translations:How to Continue After a Prayer Time/16/ar", 62225, 62270)
        execute_test("ar", "Translations:How to Continue After a Prayer Time/Page_display_title/ar", 62193, 62274)

    # TODO research which of these changes to improve Arabic language quality could be automated: 
    # https://www.4training.net/mediawiki/index.php?title=Forgiving_Step_by_Step%2Far&type=revision&diff=29760&oldid=29122

if __name__ == '__main__':
    unittest.main()

