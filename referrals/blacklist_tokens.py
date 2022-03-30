from typing import List


class BlacklistTokens:

    def __init__(self, raw_blacklist: List[str]):
        self._raw_blacklist = raw_blacklist

    def value(self) -> List[str]:
        return self._raw_blacklist
