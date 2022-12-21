import datetime
import math


def f_to_c(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    x = f - 32.0
    return x * (5 / 9)


def c_to_f(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    x = c * (9 / 5)
    return x + 32.0


TEST_VALUES = [-459.67, -273.15, 0.0, 32.0, 42.0, 273.15, 100.0, 212.0, 373.15]


def test_conversions() -> None:
    count = int(1_000_000 / len(TEST_VALUES))
    for _ in range(0, count):
        for t in TEST_VALUES:
            round_trip(t)


def round_trip(t: float) -> float:
    return f_to_c(c_to_f(t))


if __name__ == "__main__":
    t0 = datetime.datetime.now()

    test_conversions()

    t1 = datetime.datetime.now()
    dt = t1 - t0
    print(f'Done in {dt.total_seconds() * 1000:.2f} ms')
