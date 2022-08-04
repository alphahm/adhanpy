from enum import Enum
from ShadowLength import ShadowLength


class Madhab(Enum):
    """
    Shafi Madhab
    """
    SHAFI = 0

    """
    Hanafi Madhab
    """
    HANAFI = 1

    def get_shadow_length(self) -> ShadowLength:
        if self == Madhab.SHAFI:
            return ShadowLength(ShadowLength.SINGLE)
        elif self == Madhab.HANAFI:
            return ShadowLength(ShadowLength.DOUBLE)
        else:
            raise ValueError("Invalid Madhab")
