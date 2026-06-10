"""
booking.py — Book, Cancel, PNR check, History, Undo
"""

from data.data import (
    trains, bookings, seat_map, waiting_queues,
    history_stacks, current_user,
    COACH_PRICE_MULT, COACH_NAMES,
)
from utils.helpers import (
    header, pause, sep,
    gen_bid, gen_pnr,
    display_trains, display_coaches, show_seat_map, print_ticket,
)


# ─────────────────────────────────────────────
#  BOOK TICKET
# ─────────────────────────────────────────────

def book_ticket():
    uname = current_user[0]
    header("BOOK A TICKET")
    display_trains(list(trains.items()))

    tid = input("\n  Enter Train ID: ").strip().upper()
    if tid not in trains:
        print("  Train not found."); pause(); return

    t = trains[tid]
    print(f"\n  Train    : {t['name']}")
    print(f"  Route    : {t['source']} → {' → '.join(t['via'])} → {t['destination']}")
    print(f"  Date     : {t['date']}   Dep: {t['departure']}   Arr: {t['arrival']}")

    display_coaches(tid)
    coach = input("\n  Select Coach (SL / 3A / 2A / 1A): ").strip().upper()
    if coach not in seat_map[tid]:
        print("  Invalid coach."); pause(); return

    avail = sum(1 for v in seat_map[tid][coach].values() if v is None)
    if avail == 0:
        print(f"\n  No seats in {coach}. Adding you to waiting list...")
        waiting_queues[tid].enqueue((uname, coach))
        print(f"  ✓ Waiting list position: {waiting_queues[tid].size}")
        pause()
        return

    show_seat_map(tid, coach)
    seat_input = input("  Choose Seat Number: ").strip()
    if not seat_input.isdigit():
        print("  Invalid seat."); pause(); return
    seat = int(seat_input)
    if seat not in seat_map[tid][coach] or seat_map[tid][coach][seat] is not None:
        print("  Seat unavailable or already booked."); pause(); return

    # Passenger details
    n_str = input("  Number of passengers (1–4): ").strip()
    if not n_str.isdigit() or not 1 <= int(n_str) <= 4:
        print("  Invalid number."); pause(); return
    n = int(n_str)
    passengers = []
    for i in range(n):
        name = input(f"    Passenger {i+1} Name : ").strip()
        age  = input(f"    Passenger {i+1} Age  : ").strip()
        passengers.append({"name": name, "age": age})

    fare  = int(t["price"] * COACH_PRICE_MULT[coach])
    total = fare * n

    # Summary
    print(f"\n  ── Booking Summary ─────────────────────")
    print(f"  Train    : {t['name']} ({tid})")
    print(f"  Route    : {t['source']} → {t['destination']}")
    print(f"  Date     : {t['date']}  Dep: {t['departure']}")
    print(f"  Coach    : {coach} ({COACH_NAMES[coach]})   Seat: {seat}")
    for i, p in enumerate(passengers, 1):
        print(f"  Pax {i}    : {p['name']}, Age {p['age']}")
    print(f"  Fare     : ₹{fare} × {n} passenger(s) = ₹{total}")

    print("\n  Payment: 1.UPI  2.Card  3.Net Banking  4.Wallet")
    pay = input("  Choose: ").strip()
    pay_map = {"1": "UPI", "2": "Card", "3": "Net Banking", "4": "Wallet"}
    pay_mode = pay_map.get(pay, "UPI")

    confirm = input(f"\n  Confirm booking via {pay_mode}? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Booking cancelled."); pause(); return

    bid = gen_bid()
    pnr = gen_pnr()
    seat_map[tid][coach][seat] = uname
    bookings[bid] = {
        "user": uname, "train_id": tid, "coach": coach, "seat": seat,
        "status": "Confirmed", "pnr": pnr,
        "passengers": passengers, "fare": total, "payment": pay_mode,
    }
    history_stacks[uname].push(bid)
    print_ticket(bid)
    pause()


# ─────────────────────────────────────────────
#  CHECK PNR STATUS
# ─────────────────────────────────────────────

def check_pnr():
    header("CHECK PNR STATUS")
    pnr = input("  Enter PNR: ").strip().upper()
    found = next(((bid, b) for bid, b in bookings.items() if b["pnr"] == pnr), None)
    if not found:
        print("  PNR not found."); pause(); return
    bid, b = found
    t = trains[b["train_id"]]
    print(f"\n  PNR        : {b['pnr']}")
    print(f"  Status     : {b['status']}")
    print(f"  Train      : {t['name']} ({b['train_id']})")
    print(f"  Route      : {t['source']} → {t['destination']}")
    print(f"  Date       : {t['date']}   Dep: {t['departure']}")
    print(f"  Coach      : {b['coach']} ({COACH_NAMES[b['coach']]})")
    print(f"  Seat       : {b['seat']}")
    print(f"  Fare Paid  : ₹{b['fare']}")
    print(f"  Passengers :")
    for i, p in enumerate(b.get("passengers", []), 1):
        print(f"     {i}. {p['name']}  (Age: {p['age']})")
    pause()


# ─────────────────────────────────────────────
#  CANCEL TICKET
# ─────────────────────────────────────────────

def cancel_ticket():
    uname = current_user[0]
    header("CANCEL TICKET")
    my = [(bid, b) for bid, b in bookings.items()
          if b["user"] == uname and b["status"] == "Confirmed"]
    if not my:
        print("  No active bookings."); pause(); return

    print(f"\n  {'BID':<8} {'PNR':<12} {'Train':<22} {'Coach':<5} {'Seat':>5} {'Fare':>7}")
    sep("-")
    for bid, b in my:
        t = trains[b["train_id"]]
        print(f"  {bid:<8} {b['pnr']:<12} {t['name']:<22} "
              f"{b['coach']:<5} {b['seat']:>5} ₹{b['fare']:>5}")

    bid = input("\n  Booking ID to cancel: ").strip().upper()
    if (bid not in bookings or bookings[bid]["user"] != uname
            or bookings[bid]["status"] != "Confirmed"):
        print("  Invalid booking ID."); pause(); return

    b      = bookings[bid]
    refund = int(b["fare"] * 0.75)
    confirm = input(f"  Cancel {bid}? Refund ₹{refund} (25% charge). (y/n): ").strip().lower()
    if confirm != "y":
        print("  Operation cancelled."); pause(); return

    seat_map[b["train_id"]][b["coach"]][b["seat"]] = None
    b["status"] = "Cancelled"
    print(f"  ✓ Cancelled. Refund of ₹{refund} in 3–5 working days.")

    # Auto-allot from waiting list
    wq = waiting_queues[b["train_id"]]
    if not wq.is_empty():
        next_user, next_coach = wq.dequeue()
        new_bid = gen_bid()
        new_pnr = gen_pnr()
        seat_map[b["train_id"]][b["coach"]][b["seat"]] = next_user
        bookings[new_bid] = {
            "user": next_user, "train_id": b["train_id"],
            "coach": b["coach"], "seat": b["seat"],
            "status": "Confirmed", "pnr": new_pnr,
            "passengers": [{"name": next_user, "age": "N/A"}],
            "fare": b["fare"], "payment": "Auto-allotted",
        }
        if next_user in history_stacks:
            history_stacks[next_user].push(new_bid)
        print(f"  ⚡ Seat auto-allotted to waiting user: {next_user}  (PNR: {new_pnr})")
    pause()


# ─────────────────────────────────────────────
#  BOOKING HISTORY  (Stack)
# ─────────────────────────────────────────────

def view_history():
    uname = current_user[0]
    header("MY BOOKING HISTORY  [Stack — most recent first]")
    all_bkgs = history_stacks[uname].all()
    if not all_bkgs:
        print("  No bookings yet."); pause(); return
    print(f"  {'BID':<8} {'PNR':<12} {'Train':<22} "
          f"{'Coach':<5} {'Seat':>5} {'Status':<18} {'Fare':>7}")
    sep("-")
    for bid in all_bkgs:
        if bid in bookings:
            b = bookings[bid]
            t = trains[b["train_id"]]
            print(f"  {bid:<8} {b['pnr']:<12} {t['name']:<22} "
                  f"{b['coach']:<5} {b['seat']:>5} {b['status']:<18} ₹{b['fare']:>5}")
    pause()


# ─────────────────────────────────────────────
#  UNDO LAST BOOKING  (Stack Pop)
# ─────────────────────────────────────────────

def undo_last_booking():
    uname = current_user[0]
    header("UNDO LAST BOOKING  [Stack Pop]")
    stack = history_stacks[uname]
    if stack.is_empty():
        print("  Nothing to undo."); pause(); return
    bid = stack.peek()
    b   = bookings.get(bid)
    if not b or b["status"] != "Confirmed":
        print(f"  Last booking {bid} is already {b['status'] if b else 'invalid'}."); pause(); return
    t = trains[b["train_id"]]
    print(f"  Last booking : {bid}  |  {t['name']}  |  Seat {b['seat']}  |  ₹{b['fare']}")
    if input("  Undo (cancel) this booking? (y/n): ").strip().lower() == "y":
        seat_map[b["train_id"]][b["coach"]][b["seat"]] = None
        b["status"] = "Cancelled (Undo)"
        stack.pop()
        print(f"  ✓ Booking {bid} undone. Full refund of ₹{b['fare']} processed.")
    pause()
