class ShadowLength:
    SINGLE = 1.0
    DOUBLE = 2.0

    def __init__(self, shadow_length):
        self._shadow_length = shadow_length

    @property
    def shadow_length(self):
        return self._shadow_length
