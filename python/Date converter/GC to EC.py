from typing import Tuple


def is_gregorian_leap(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_in_month_greg(year: int, month: int) -> int:
    if month < 1 or month > 12:
        raise ValueError("Month must be 1..12")
    dim = [31, 29 if is_gregorian_leap(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return dim[month - 1]


def day_of_year(year: int, month: int, day: int) -> int:
    # Assumes valid date
    acc = 0
    for m in range(1, month):
        acc += days_in_month_greg(year, m)
    return acc + day


def gregorian_eny_doy(year: int) -> int:
    """Day-of-year for Ethiopian New Year (Meskerem 1) in Gregorian year.

    Rule: ENY falls on Sep 11, or on Sep 12 if the NEXT Gregorian year is leap.
    """
    # Compute DOY for Sep 11 and Sep 12 in this Gregorian year
    sep11 = day_of_year(year, 9, 11)
    sep12 = day_of_year(year, 9, 12)
    return sep12 if is_gregorian_leap(year + 1) else sep11


def convert_gc_to_ec(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """Convert Gregorian date -> Ethiopian date (year, month, day).

    - Validates the input Gregorian date.
    - Uses ENY rule (Sep 11, or Sep 12 if next GC year is leap).
    - Returns Ethiopian year, month (1..13), and day (1..30; month 13 has 5 or 6 days).
    """
    if year < 1:
        raise ValueError("Year must be >= 1")
    if month < 1 or month > 12:
        raise ValueError("Month must be 1..12")
    max_day = days_in_month_greg(year, month)
    if day < 1 or day > max_day:
        raise ValueError(f"Invalid day for {year}-{month:02d}: must be 1..{max_day}")

    doy = day_of_year(year, month, day)
    eny_curr = gregorian_eny_doy(year)

    if doy >= eny_curr:
        # On/after ENY of this GC year -> Ethiopian year is (GC year - 7)
        days_since_eny = doy - eny_curr
        eth_year = year - 7
    else:
        # Before ENY -> measure from ENY in previous GC year
        eny_prev = gregorian_eny_doy(year - 1)
        days_in_prev_gc_year = 366 if is_gregorian_leap(year - 1) else 365
        days_since_eny = (days_in_prev_gc_year - eny_prev) + doy
        eth_year = year - 8

    eth_month = (days_since_eny // 30) + 1  # 1..13
    eth_day = (days_since_eny % 30) + 1     # 1..30 (month 13 has 5/6 days)

    return eth_year, eth_month, eth_day


def _prompt_int(prompt: str) -> int:
    val = int(input(prompt))
    return val


if __name__ == "__main__":
    print("Enter Gregorian date (GC)")
    try:
        d = _prompt_int("Day (1-31): ")
        m = _prompt_int("Month (1-12): ")
        y = _prompt_int("Year (>=1): ")
        ey, em, ed = convert_gc_to_ec(y, m, d)
        print(f"Ethiopian (EC): {ed:02d}-{em:02d}-{ey}")
    except Exception as e:
        print(f"Error: {e}")