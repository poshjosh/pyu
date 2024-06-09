import unittest

from pyu.io.logging import SecretsMaskingFilter


class LoggingTestCase(unittest.TestCase):
    patterns: [str] = \
        ["(pass|key|secret|token|jwt|hash|signature|credential|auth|certificate|connection|pat)"]
    mask = "*******"

    def masker(self, _, __):
        return self.mask

    def test_secrets_masking(self):
        secrets_masking_filter = SecretsMaskingFilter(self.patterns, self.masker)

        target: str = """Üwe
This is a test string with PASSWORD
is
connection details
HAPPY
\tSecret details
"""
        actual = secrets_masking_filter.redact(target)
        expected = f"""Üwe
{self.mask}
is
{self.mask}
HAPPY
{self.mask}
"""
        self.assertEqual(expected, actual)

    def test_secrets_masking_number(self):
        self.assertEqual(123, SecretsMaskingFilter(self.patterns).redact(123))

    def test_secrets_masking_dict(self):
        secrets_masking_filter = SecretsMaskingFilter(self.patterns, self.masker)
        target: dict = {"name": "Test", "arg": "password", "key": "value"}
        expected: dict = {"name": "Test", "arg": self.mask, self.mask: "value"}
        actual = secrets_masking_filter.redact(target)
        self.assertEqual(expected, actual)

    def test_secrets_masking_iter(self):
        secrets_masking_filter = SecretsMaskingFilter(self.patterns, self.masker)
        target: iter = ["Test", "password", "value"]
        expected: iter = ["Test", self.mask, "value"]
        actual = secrets_masking_filter.redact(target)
        self.assertEqual(expected, actual)

    class CustomObj:
        def __str__(self):
            return "Contains a secret"

    def test_secrets_masking_obj(self):
        secrets_masking_filter = SecretsMaskingFilter(self.patterns, self.masker)
        target = LoggingTestCase.CustomObj()
        actual = secrets_masking_filter.redact(target)
        self.assertEqual(self.mask, actual)


if __name__ == '__main__':
    unittest.main()
