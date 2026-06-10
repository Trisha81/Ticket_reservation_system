"""
helpers.py — Shared utility functions
"""

from data.data import (
    trains, bookings, seat_map, history_stacks,
    booking_counter, pnr_counter,
    COACH_PRICE_MULT, COACH_NAMES,
)


def sep(c="─", n=60):
    print(c * n)


def header(title):
    sep("═")
    print(f"   {title}")
    sep("═")


def pause():
    input("\n  [Press Enter to continue]")


def gen_bid():
    booking_counter[0] += 1
    return f"BK{booking_counter[0]}"


def gen_pnr():
    pnr_counter[0] += 1
    return f"PNR{pnr_counter[0]}"


def display_trains(train_list):
    if not train_list:
        print("  No trains found.")
        return
    print(f"\n  {'ID':<8} {'Train Name':<22} {'From':<12} {'To':<12} "
          f"{'Date':<12} {'Dep':>6} {'Arr':>6} {'Base ₹':>8}")
    sep("-")
    for tid, t in train_list:
        print(f"  {tid:<8} {t['name']:<22} {t['source']:<12} "
              f"{t['destination']:<12} {t['date']:<12} "
              f"{t['departure']:>6} {t['arrival']:>6} ₹{t['price']:>6}")


def display_coaches(tid):
    t = trains[tid]
    print(f"\n  Coaches for {t['name']} ({tid}):")
    print(f"  {'Coach':<6} {'Type':<16} {'Available':>10} {'Price':>10}")
    sep("-")
    for coach, seats in seat_map[tid].items():
        avail = sum(1 for v in seats.values() if v is None)
        price = int(t["price"] * COACH_PRICE_MULT[coach])
        print(f"  {coach:<6} {COACH_NAMES[coach]:<16} {avail:>10} ₹{price:>8}")


def show_seat_map(tid, coach):
    seats = seat_map[tid][coach]
    print(f"\n  Seat Map — {trains[tid]['name']} | "
          f"Coach: {coach} ({COACH_NAMES[coach]})")
    sep("-")
    print("  [ ] = Available   [X] = Booked\n")
    for i, (sno, occ) in enumerate(seats.items(), 1):
        mark = "[X]" if occ else "[ ]"
        print(f"  {sno:>2}{mark}", end="   ")
        if i % 6 == 0:
            print()
    print("\n")


def print_ticket(bid):
    b = bookings[bid]
    t = trains[b["train_id"]]
    print(f"\n  ╔══════════════════════════════════════╗")
    print(f"  ║        BOOKING CONFIRMED  ✓          ║")
    print(f"  ╠══════════════════════════════════════╣")
    print(f"  ║  PNR        : {b['pnr']:<23}║")
    print(f"  ║  Booking ID : {bid:<23}║")
    print(f"  ║  Train      : {t['name']:<23}║")
    print(f"  ║  Route      : {t['source']+' → '+t['destination']:<23}║")
    print(f"  ║  Date       : {t['date']:<23}║")
    print(f"  ║  Departure  : {t['departure']:<23}║")
    print(f"  ║  Coach      : {b['coach']:<23}║")
    print(f"  ║  Seat       : {str(b['seat']):<23}║")
    print(f"  ║  Passengers : {str(len(b['passengers'])):<23}║")
    print(f"  ║  Amount     : ₹{str(b['fare']):<22}║")
    print(f"  ║  Payment    : {b['payment']:<23}║")
    print(f"  ╚══════════════════════════════════════╝")
