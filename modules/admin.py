"""
admin.py — Admin panel
"""

from data.data import (
    users, trains, bookings, seat_map,
    waiting_queues, price_bst,
    DEFAULT_COACHES,
)
from modules.dsa import Queue
from modules.search import bst_traversals, view_station_network
from utils.helpers import header, pause, sep
from modules.booking import check_pnr


ADMIN_PASSWORD = "admin123"


def admin_panel():
    header("ADMIN LOGIN")
    if input("  Password: ").strip() != ADMIN_PASSWORD:
        print("  Wrong password."); pause(); return

    while True:
        header("ADMIN PANEL")
        print("  1.  View All Bookings")
        print("  2.  View All Users")
        print("  3.  Add New Train")
        print("  4.  View Waiting Lists  [Queue]")
        print("  5.  BST Traversals      [Inorder / Preorder / Postorder]")
        print("  6.  Station Network     [Graph]")
        print("  7.  Revenue Report")
        print("  8.  Search Booking by PNR")
        print("  9.  Back")
        sep()
        ch = input("  Choice: ").strip()

        if ch == "1":
            header("ALL BOOKINGS")
            if not bookings:
                print("  No bookings yet.")
            else:
                print(f"  {'BID':<8} {'PNR':<12} {'User':<12} {'Train':<22} "
                      f"{'Coach':<5} {'Seat':>5} {'Status':<18} {'Fare':>7}")
                sep("-")
                for bid, b in bookings.items():
                    t = trains[b["train_id"]]
                    print(f"  {bid:<8} {b['pnr']:<12} {b['user']:<12} "
                          f"{t['name']:<22} {b['coach']:<5} {b['seat']:>5} "
                          f"{b['status']:<18} ₹{b['fare']:>5}")
            pause()

        elif ch == "2":
            header("ALL USERS")
            if not users:
                print("  No users registered.")
            else:
                print(f"  {'Username':<15} {'Email':<28} {'Phone'}")
                sep("-")
                for u, info in users.items():
                    print(f"  {u:<15} {info['email']:<28} {info['phone']}")
            pause()

        elif ch == "3":
            header("ADD NEW TRAIN")
            tid   = input("  Train ID    : ").strip().upper()
            name  = input("  Train Name  : ").strip()
            src   = input("  Source      : ").strip()
            dest  = input("  Destination : ").strip()
            date  = input("  Date        : ").strip()
            dep   = input("  Departure   : ").strip()
            arr   = input("  Arrival     : ").strip()
            price = int(input("  Base Price ₹: ").strip())
            trains[tid] = {
                "name": name, "source": src, "destination": dest, "via": [],
                "date": date, "departure": dep, "arrival": arr,
                "price": price, "coaches": dict(DEFAULT_COACHES),
            }
            seat_map[tid] = {
                c: {i: None for i in range(1, n + 1)}
                for c, n in DEFAULT_COACHES.items()
            }
            waiting_queues[tid] = Queue()
            price_bst.insert(price, tid)
            print(f"  ✓ Train {tid} added and inserted into BST.")
            pause()

        elif ch == "4":
            header("WAITING LISTS  [Queue]")
            any_waiting = False
            for tid, wq in waiting_queues.items():
                wlist = wq.to_list()
                if wlist:
                    any_waiting = True
                    t = trains[tid]
                    names = ", ".join(str(x) for x in wlist[:5])
                    print(f"  {tid} ({t['name']}): {len(wlist)} waiting  [{names}]")
            if not any_waiting:
                print("  No one is on the waiting list.")
            pause()

        elif ch == "5":
            bst_traversals()

        elif ch == "6":
            view_station_network()

        elif ch == "7":
            header("REVENUE REPORT")
            confirmed = [b for b in bookings.values() if b["status"] == "Confirmed"]
            cancelled = [b for b in bookings.values() if "Cancelled" in b["status"]]
            total_rev = sum(b["fare"] for b in confirmed)
            print(f"\n  Total Confirmed Bookings : {len(confirmed)}")
            print(f"  Total Cancellations      : {len(cancelled)}")
            print(f"  Total Revenue            : ₹{total_rev}")
            print(f"\n  Per-Train Breakdown:")
            sep("-")
            for tid, t in trains.items():
                rev = sum(b["fare"] for b in confirmed if b["train_id"] == tid)
                cnt = sum(1 for b in confirmed if b["train_id"] == tid)
                bar = "█" * min(cnt * 2, 30)
                print(f"  {t['name']:<25} {cnt:>3} bookings  ₹{rev:>8}  {bar}")
            pause()

        elif ch == "8":
            check_pnr()

        elif ch == "9":
            break
