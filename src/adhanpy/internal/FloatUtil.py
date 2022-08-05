import math


def normalize_with_bound(value, max):
    return value - (max * (math.floor(value / max)))


def unwind_angle(value):
    return normalize_with_bound(value, 360)


def closest_angle(angle):
    if angle >= -180 and angle <= 180:
        return angle

    return angle - (360 * round(angle / 360))
