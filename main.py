"""
main.py — Entry point for the Train Reservation System

Run:
    python main.py

DSA Used:
    Stack, Queue (Linked List), BST (Inorder/Preorder/Postorder),
    Graph (BFS + DFS), Linear Search, Binary Search, Hash Map
"""

import sys
import os

# Make sure all folders are importable
sys.path.insert(0, os.path.dirname(__file__))

from modules.auth    import register, login, logout
from modules.booking import book_ticket, cancel_ticket, check_pnr, view_history, undo_last_booking
from modules.search  import (search_by_route, search_by_name, search_by_id,
                              search_by_price, bst_traversals,
                              view_station_network, find_path)
from modules.admin   import admin_panel
from data.data       import trains, current_user
from utils.helpers   import header, sep, pause, display_trains


# ─────────────────────────────────────────────
#  USER MENU
# ─────────────────────────────────────────────

def user_menu():
    while True:
        header(f"TRAIN RESERVATION SYSTEM   [ User: {current_user[0]} ]")
        print("  ── Search ───────────────────────────────────")
        print("  1.  View All Trains")
        print("  2.  Search by Source / Destination  [Linear Search]")
        print("  3.  Search by Train Name            [Linear Search]")
        print("  4.  Search by Train ID              [Binary Search]")
        print("  5.  Search by Price Range           [BST]")
        print("  ── DSA Visualiser ───────────────────────────")
        print("  6.  BST Traversals  (Inorder / Preorder / Postorder)")
        print("  7.  Station Network  [Graph — Adjacency List]")
        print("  8.  Find Path Between Stations  [BFS + DFS]")
        print("  ── Booking ──────────────────────────────────")
        print("  9.  Book a Ticket")
        print("  10. Check PNR Status")
        print("  11. Cancel Ticket")
        print("  12. My Booking History    [Stack]")
        print("  13. Undo Last Booking     [Stack Pop]")
        print("  ─────────────────────────────────────────────")
        print("  14. Logout")
        sep()
        ch = input("  Choice: ").strip()

        if   ch == "1":  display_trains(list(trains.items())); pause()
        elif ch == "2":  search_by_route()
        elif ch == "3":  search_by_name()
        elif ch == "4":  search_by_id()
        elif ch == "5":  search_by_price()
        elif ch == "6":  bst_traversals()
        elif ch == "7":  view_station_network()
        elif ch == "8":  find_path()
        elif ch == "9":  book_ticket()
        elif ch == "10": check_pnr()
        elif ch == "11": cancel_ticket()
        elif ch == "12": view_history()
        elif ch == "13": undo_last_booking()
        elif ch == "14": logout(); break
        else:            print("  Invalid choice.")


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

def main():
    while True:
        sep("═")
        print("        INDIAN RAILWAY RESERVATION SYSTEM")
        print("                 [ DSA PROJECT ]")
        sep("═")
        print("  1. Register")
        print("  2. Login")
        print("  3. Admin Panel  (password: admin123)")
        print("  4. Exit")
        sep("═")
        ch = input("  Choice: ").strip()

        if   ch == "1": register()
        elif ch == "2":
            if login(): user_menu()
        elif ch == "3": admin_panel()
        elif ch == "4": print("\n  Thank You! Jai Hind! 🇮🇳\n"); break
        else:           print("  Invalid choice.")


if __name__ == "__main__":
    main()
