from jsonsubschema._canonicalization import simplify_schema_and_embed_checkers
from jsonsubschema._checkers import JSONbot, JSONtop, is_bot, is_top
import unittest


class TestIsTop(unittest.TestCase):
    def test_true_is_top(self) -> None:
        self.assertTrue(is_top(True))

    def test_empty_object_is_top(self) -> None:
        self.assertTrue(is_top({}))

    def test_json_top_is_top(self) -> None:
        self.assertTrue(is_top(JSONtop()))

    def test_one_is_not_top(self) -> None:
        self.assertFalse(is_top(1))


class TestIsBot(unittest.TestCase):
    def test_false_is_bot(self) -> None:
        self.assertTrue(is_bot(False))

    def test_not_empty_object_is_bot(self) -> None:
        self.assertTrue(is_bot({"not": {}}))

    def test_json_bot_is_bot(self) -> None:
        self.assertTrue(is_bot(JSONbot()))

    def test_uninhabited_schema_is_bot(self) -> None:
        uninhabited_schema = simplify_schema_and_embed_checkers({"type": "integer", "minimum": 2, "maximum": 1})
        self.assertTrue(is_bot(uninhabited_schema))

    def test_zero_is_not_bot(self) -> None:
        self.assertFalse(is_bot(0))
