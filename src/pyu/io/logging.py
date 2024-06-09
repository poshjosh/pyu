import logging
import os
import re
from collections.abc import Iterable
from typing import Callable, Union, List


class SecretsMaskingFilter(logging.Filter):
    def __init__(self,
                 patterns: [str],
                 mask_line: Union[Callable[[str, List[re.Match]], str], None] = None):
        super(SecretsMaskingFilter, self).__init__()
        self.__patterns: [str] = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        self.__mask_line: Union[Callable[[str, List[re.Match]], str], None] = mask_line \
            if mask_line is not None else lambda line, matches: "<*** masked ***>"

    def filter(self, record):
        record.msg = self.redact(record.msg)
        record.args = self.redact(record.args)
        return True

    def redact(self, value: any) -> any:
        if value is None:
            return value
        if isinstance(value, str):
            return self.__redact_str(value)
        elif isinstance(value, dict):
            return {self.redact(k): self.redact(v) for k, v in value.items()}
        elif isinstance(value, tuple):
            return tuple(self.redact(e) for e in value)
        elif isinstance(value, Iterable):
            return [self.redact(v) for v in value]
        else:
            original: str = str(value)
            redacted = self.__redact_str(original)
            return value if redacted == original else redacted

    def __redact_str(self, sval: str) -> any:
        if sval is None:
            return None
        lines: [str] = sval.split(os.linesep)
        redacted: int = 0
        for i, line in enumerate(lines):
            matches = self.__matches(line)
            if len(matches) > 0:
                lines[i] = self.__mask_line(line, matches)
                redacted += 1
            else:
                lines[i] = line
        return sval if redacted == 0 else os.linesep.join(lines)

    def __matches(self, line: str) -> List[re.Match]:
        matches: List[re.Match] = list()
        for pattern in self.__patterns:
            match = pattern.search(line)
            if match:
                matches.append(match)
        return matches
