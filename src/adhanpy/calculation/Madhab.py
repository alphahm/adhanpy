from enum import Enum
from adhanpy.data.ShadowLength import ShadowLength


class Madhab(Enum):

    SHAFI = 0
    # Shafi Madhab

    HANAFI = 1
    # Hanafi Madhab

    def get_shadow_length(self) -> ShadowLength:
        if self == Madhab.SHAFI:
            return ShadowLength(ShadowLength.SINGLE)
        elif self == Madhab.HANAFI:
            return ShadowLength(ShadowLength.DOUBLE)
