"""obviously these don't cover all of the cases"""

import regexp
import unittest


class TestMatchEqLen(unittest.TestCase):
    def test_match_eq1(self):
        self.assertTrue(regexp.match_eq("apple", "apple"))

    def test_match_eq2(self):
        self.assertTrue(regexp.match_eq(".pple", "apple"))

    def test_match_eq3(self):
        self.assertTrue(regexp.match_eq("appl.", "apple"))

    def test_match_eq4(self):

        self.assertTrue(regexp.match_eq(".....", "apple"))

    def test_match_eq5(self):

        self.assertFalse(regexp.match_eq("peach", "apple"))


class TestMatchUneqLen(unittest.TestCase):
    def test_match_uneq1(self):
        self.assertTrue(regexp.match_uneq("apple", "apple"))

    def test_match_uneq2(self):
        self.assertTrue(regexp.match_uneq("ap", "apple"))

    def test_match_uneq3(self):
        self.assertTrue(regexp.match_uneq("le", "apple"))

    def test_match_uneq4(self):

        self.assertTrue(regexp.match_uneq("a", "apple"))

    def test_match_uneq5(self):

        self.assertTrue(regexp.match_uneq(".", "apple"))

    def test_match_uneq6(self):

        self.assertFalse(regexp.match_uneq("apwle", "apple"))

    def test_match_uneq7(self):

        self.assertFalse(regexp.match_uneq("peach", "apple"))


class TestMatchPos(unittest.TestCase):
    def test_match_pos1(self):
        self.assertTrue(regexp.match("apple", "apple"))

    def test_match_pos2(self):
        self.assertTrue(regexp.match("^app", "apple"))

    def test_match_pos3(self):
        self.assertTrue(regexp.match("le$", "apple"))

    def test_match_pos4(self):
        self.assertTrue(regexp.match("^a", "apple"))

    def test_match_pos5(self):
        self.assertTrue(regexp.match(".$", "apple"))

    def test_match_pos6(self):
        self.assertTrue(regexp.match("apple$", "tasty apple"))

    def test_match_pos7(self):
        self.assertTrue(regexp.match("^apple", "apple pie"))

    def test_match_pos8(self):
        self.assertTrue(regexp.match("^apple$", "apple"))

    def test_match_pos9(self):
        self.assertFalse(regexp.match("^apple$", "tasty apple"))

    def test_match_pos10(self):
        self.assertFalse(regexp.match("^apple$", "apple pie"))

    def test_match_pos11(self):
        self.assertFalse(regexp.match("app$", "apple"))

    def test_match_pos12(self):
        self.assertFalse(regexp.match("^le", "apple"))


class TestMatchQuant(unittest.TestCase):
    def test_match_quant1(self):
        self.assertTrue(regexp.match("colou?r", "color"))

    def test_match_quant2(self):
        self.assertTrue(regexp.match("colou?r", "colour"))

    def test_match_quant3(self):
        self.assertFalse(regexp.match("colou?r", "colouur"))

    def test_match_quant4(self):
        self.assertTrue(regexp.match("colou*r", "color"))

    def test_match_quant5(self):
        self.assertTrue(regexp.match("colou*r", "colour"))

    def test_match_quant6(self):
        self.assertTrue(regexp.match("colou*r", "colouur"))

    def test_match_quant7(self):
        self.assertTrue(regexp.match("col.*r", "color"))

    def test_match_quant8(self):
        self.assertTrue(regexp.match("col.*r", "colour"))

    def test_match_quant9(self):
        self.assertTrue(regexp.match("col.*r", "colr"))

    def test_match_quant10(self):
        self.assertTrue(regexp.match("col.*r", "collar"))

    def test_match_quant11(self):
        self.assertFalse(regexp.match("col.*r$", "colors"))


if __name__ == "__main__":
    unittest.main()