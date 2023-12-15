import unittest

from jsonsubschema import isSubschema
from jsonsubschema.exceptions import UnsupportedEnumCanonicalization


class TestConst(unittest.TestCase):
    def test_const_equal_num(self) -> None:
        s1 = {"const": 1}
        s2 = {"const": 1}

        with self.subTest("LHS < RHS"):
            assert isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert isSubschema(s2, s1)

    def test_const_equal_str(self) -> None:
        s1 = {"const": "a"}
        s2 = {"const": "a"}

        with self.subTest("LHS < RHS"):
            assert isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert isSubschema(s2, s1)

    def test_const_vs_enum(self) -> None:
        s1 = {"const": 1}
        s2 = {"enum": [1, 2]}

        with self.subTest("LHS < RHS"):
            assert isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert not isSubschema(s2, s1)

    def test_const_vs_wrong_enum(self) -> None:
        s1 = {"const": 1}
        s2 = {"enum": [2, 3]}

        with self.subTest("LHS < RHS"):
            assert not isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert not isSubschema(s2, s1)

    def test_const_vs_type(self) -> None:
        s1 = {"const": 1}
        s2 = {"type": "integer"}

        with self.subTest("LHS < RHS"):
            assert isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert not isSubschema(s2, s1)

    def test_const_vs_wrong_type(self) -> None:
        s1 = {"const": 1}
        s2 = {"type": "string"}

        with self.subTest("LHS < RHS"):
            assert not isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert not isSubschema(s2, s1)

    def test_const_type_mix(self) -> None:
        s1 = {"const": "1"}
        s2 = {"const": 1}

        with self.subTest("LHS < RHS"):
            assert not isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert not isSubschema(s2, s1)

    def test_enum_uninhabited1(self) -> None:
        s1 = {"type": "string", "const": 1}
        s2 = {"type": "string"}

        with self.subTest("LHS < RHS"):
            assert isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert not isSubschema(s2, s1)

    def test_enum_uninhabited2(self) -> None:
        s1 = {"type": "string", "const": 1}
        s2 = {"type": "boolean", "const": 1}

        with self.subTest("LHS < RHS"):
            assert isSubschema(s1, s2)
        with self.subTest("LHS > RHS"):
            assert isSubschema(s2, s1)


class TestEnumNotSupported(unittest.TestCase):
    def test_array(self) -> None:
        s1 = {"const": []}
        s2 = {"type": "array"}

        with self.subTest():
            self.assertRaises(UnsupportedEnumCanonicalization, isSubschema, s1, s2)

        with self.subTest():
            self.assertRaises(UnsupportedEnumCanonicalization, isSubschema, s2, s1)

    def test_object(self) -> None:
        s1 = {"const": {}}
        s2 = {"type": "object"}

        with self.subTest():
            self.assertRaises(UnsupportedEnumCanonicalization, isSubschema, s1, s2)

        with self.subTest():
            self.assertRaises(UnsupportedEnumCanonicalization, isSubschema, s2, s1)
