"""
search.py — All search features
  • Search by source/destination  (Linear Search)
  • Search by train name           (Linear Search)
  • Search by train ID             (Binary Search)
  • Search by price range          (BST range query)
  • BST Traversals                 (Inorder / Preorder / Postorder)
  • Station path finder            (BFS + DFS on Graph)
"""

from data.data import trains, price_bst, station_graph
from modules.dsa import binary_search_train
from utils.helpers import header, pause, sep, display_trains


# ─────────────────────────────────────────────
#  LINEAR SEARCH — by source / destination
# ─────────────────────────────────────────────

def search_by_route():
    header("SEARCH BY SOURCE / DESTINATION  [Linear Search]")
    src  = input("  Source      (blank = any): ").strip()
    dest = input("  Destination (blank = any): ").strip()
    results = [
        (tid, t) for tid, t in trains.items()
        if (not src  or t["source"].lower()      == src.lower()) and
           (not dest or t["destination"].lower()  == dest.lower())
    ]
    display_trains(results)
    pause()


# ─────────────────────────────────────────────
#  LINEAR SEARCH — by train name keyword
# ─────────────────────────────────────────────

def search_by_name():
    header("SEARCH TRAIN BY NAME  [Linear Search]")
    query = input("  Enter train name keyword: ").strip().lower()
    results = [
        (tid, t) for tid, t in trains.items()
        if query in t["name"].lower()
    ]
    display_trains(results)
    pause()


# ─────────────────────────────────────────────
#  BINARY SEARCH — by exact train ID
# ─────────────────────────────────────────────

def search_by_id():
    header("SEARCH BY TRAIN ID  [Binary Search]")
    sorted_ids = sorted(trains.keys())
    print(f"  Available IDs (sorted): {sorted_ids}\n")
    target = input("  Enter exact Train ID: ").strip().upper()
    idx = binary_search_train(sorted_ids, target)
    if idx == -1:
        print(f"  ✗ Train '{target}' not found.")
    else:
        print(f"  ✓ Found at index {idx} in sorted list!")
        display_trains([(target, trains[target])])
    pause()


# ─────────────────────────────────────────────
#  BST RANGE SEARCH — by price
# ─────────────────────────────────────────────

def search_by_price():
    header("SEARCH BY PRICE RANGE  [BST Range Query]")
    try:
        lo = int(input("  Min price ₹: ").strip())
        hi = int(input("  Max price ₹: ").strip())
    except ValueError:
        print("  Invalid input."); pause(); return
    results = price_bst.search_range(lo, hi)
    if not results:
        print(f"  No trains found in ₹{lo}–₹{hi} range.")
    else:
        print(f"\n  Trains priced ₹{lo} – ₹{hi}:")
        sep("-")
        for price, tid in results:
            t = trains[tid]
            print(f"  {tid}  {t['name']:<22}  "
                  f"{t['source']} → {t['destination']}  ₹{price}")
    pause()


# ─────────────────────────────────────────────
#  BST TRAVERSALS
# ─────────────────────────────────────────────

def bst_traversals():
    header("BST TRAVERSALS  (Trains indexed by Base Price)")
    print("  Each train was inserted into a BST by its base price.")
    print("  Left subtree = cheaper trains, Right = costlier trains.\n")

    print("  ── INORDER  (Left → Root → Right)  →  Ascending Price ──")
    for price, tid in price_bst.inorder():
        print(f"     ₹{price:>5}  │  {tid}  │  {trains[tid]['name']}")

    print("\n  ── PREORDER  (Root → Left → Right)  →  Root first ──")
    for price, tid in price_bst.preorder():
        print(f"     ₹{price:>5}  │  {tid}  │  {trains[tid]['name']}")

    print("\n  ── POSTORDER  (Left → Right → Root)  →  Leaves first ──")
    for price, tid in price_bst.postorder():
        print(f"     ₹{price:>5}  │  {tid}  │  {trains[tid]['name']}")
    pause()


# ─────────────────────────────────────────────
#  GRAPH — Station Network
# ─────────────────────────────────────────────

def view_station_network():
    header("STATION NETWORK  [Graph — Adjacency List]")
    station_graph.display()
    pause()


# ─────────────────────────────────────────────
#  GRAPH — Path Finder (BFS + DFS)
# ─────────────────────────────────────────────

def find_path():
    header("FIND PATH BETWEEN STATIONS  [BFS + DFS]")
    all_stations = sorted(station_graph.adj.keys())
    print("  Stations:", ", ".join(all_stations))
    src  = input("\n  From Station: ").strip().title()
    dest = input("  To   Station: ").strip().title()

    print("\n  ── BFS  (Shortest Path — fewest stops) ──")
    path = station_graph.bfs_path(src, dest)
    if path:
        print("  " + " → ".join(path))
        print(f"  Total stops: {len(path) - 1}")
    else:
        print("  No path found.")

    print("\n  ── DFS  (All Possible Paths) ──")
    all_paths = station_graph.dfs_all_paths(src, dest)
    if all_paths:
        for i, p in enumerate(all_paths[:6], 1):
            print(f"  Path {i}: " + " → ".join(p))
        if len(all_paths) > 6:
            print(f"  ... and {len(all_paths) - 6} more paths.")
    else:
        print("  No paths found.")
    pause()
