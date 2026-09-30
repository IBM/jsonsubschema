import unittest

from jsonsubschema import is_subschema_with_reason, SubschemaResult


class TestExplainAPI(unittest.TestCase):
    def test_subschema_returns_true_with_empty_reasons(self):
        s1 = {"type": "integer"}
        s2 = {"type": ["integer", "string"]}
        result = is_subschema_with_reason(s1, s2)

        self.assertIsInstance(result, SubschemaResult)
        self.assertTrue(result.is_subtype)
        self.assertEqual(result.reasons, [])

    def test_result_usable_in_boolean_context(self):
        s1 = {"type": "integer"}
        s2 = {"type": ["integer", "string"]}
        result = is_subschema_with_reason(s1, s2)

        self.assertTrue(result)
        self.assertTrue(bool(result))

    def test_not_subschema_returns_false(self):
        s1 = {"type": "string"}
        s2 = {"type": "integer"}
        result = is_subschema_with_reason(s1, s2)

        self.assertIsInstance(result, SubschemaResult)
        self.assertFalse(result.is_subtype)

    def test_not_subschema_usable_in_boolean_context(self):
        s1 = {"type": "string"}
        s2 = {"type": "integer"}
        result = is_subschema_with_reason(s1, s2)

        self.assertFalse(result)
        self.assertFalse(bool(result))

    def test_numeric_constraint_failure_captured(self):
        s1 = {"type": "integer", "minimum": 0, "maximum": 100}
        s2 = {"type": "integer", "minimum": 0, "maximum": 50}
        result = is_subschema_with_reason(s1, s2)

        self.assertFalse(result.is_subtype)
        self.assertGreater(len(result.reasons), 0)
        reason_text = " ".join(result.reasons)
        self.assertIn("num__", reason_text)

    def test_array_items_failure_captured(self):
        s1 = {"type": "array", "items": {"type": "integer"}}
        s2 = {"type": "array", "items": {"type": "integer", "maximum": 10}}
        result = is_subschema_with_reason(s1, s2)

        self.assertFalse(result.is_subtype)
        self.assertGreater(len(result.reasons), 0)

    def test_object_property_constraint_failure_captured(self):
        s1 = {
            "type": "object",
            "properties": {"count": {"type": "integer"}},
            "required": ["count"],
        }
        s2 = {
            "type": "object",
            "properties": {"count": {"type": "integer", "maximum": 10}},
            "required": ["count"],
        }
        result = is_subschema_with_reason(s1, s2)

        self.assertFalse(result.is_subtype)
        self.assertGreater(len(result.reasons), 0)

    def test_identical_schemas_are_subtypes(self):
        s1 = {"type": "object", "properties": {"id": {"type": "integer"}}}
        s2 = {"type": "object", "properties": {"id": {"type": "integer"}}}
        result = is_subschema_with_reason(s1, s2)

        self.assertTrue(result.is_subtype)
        self.assertEqual(result.reasons, [])


class TestSubschemaResultDataclass(unittest.TestCase):
    def test_result_fields(self):
        result = SubschemaResult(is_subtype=True, reasons=[])
        self.assertTrue(result.is_subtype)
        self.assertEqual(result.reasons, [])

    def test_result_with_reasons(self):
        reasons = ["reason1", "reason2"]
        result = SubschemaResult(is_subtype=False, reasons=reasons)
        self.assertFalse(result.is_subtype)
        self.assertEqual(result.reasons, reasons)

    def test_default_reasons_is_empty_list(self):
        result = SubschemaResult(is_subtype=True)
        self.assertEqual(result.reasons, [])


if __name__ == "__main__":
    unittest.main()
