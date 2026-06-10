"""
data.py — Seed data: trains, station graph, coach constants
"""

from modules.dsa import BST, Graph, Queue, Stack

# ─────────────────────────────────────────────
#  COACH CONSTANTS
# ─────────────────────────────────────────────

COACH_PRICE_MULT = {"SL": 1.0, "3A": 1.5, "2A": 2.0, "1A": 3.0}
COACH_NAMES      = {
    "SL": "Sleeper",
    "3A": "AC 3 Tier",
    "2A": "AC 2 Tier",
    "1A": "AC First Class",
}
DEFAULT_COACHES  = {"SL": 40, "3A": 30, "2A": 20, "1A": 10}

# ─────────────────────────────────────────────
#  TRAINS
# ─────────────────────────────────────────────

trains = {
    "EXP101": {
        "name": "Rajdhani Express",
        "source": "Delhi", "destination": "Mumbai",
        "via": ["Agra", "Kota", "Vadodara"],
        "date": "2026-07-10", "departure": "06:00", "arrival": "22:00",
        "price": 1500, "coaches": {"SL": 40, "3A": 30, "2A": 20, "1A": 10},
    },
    "EXP102": {
        "name": "Shatabdi Express",
        "source": "Mumbai", "destination": "Chennai",
        "via": ["Pune", "Goa", "Mangalore"],
        "date": "2026-07-11", "departure": "07:30", "arrival": "21:30",
        "price": 1200, "coaches": {"SL": 40, "3A": 30, "2A": 20, "1A": 10},
    },
    "EXP103": {
        "name": "Duronto Express",
        "source": "Delhi", "destination": "Kolkata",
        "via": ["Kanpur", "Allahabad", "Asansol"],
        "date": "2026-07-12", "departure": "14:00", "arrival": "06:00",
        "price": 1100, "coaches": {"SL": 40, "3A": 30, "2A": 20, "1A": 10},
    },
    "EXP104": {
        "name": "Garib Rath",
        "source": "Chennai", "destination": "Delhi",
        "via": ["Vijayawada", "Nagpur", "Bhopal"],
        "date": "2026-07-13", "departure": "18:00", "arrival": "10:00",
        "price": 800, "coaches": {"SL": 40, "3A": 30, "2A": 20, "1A": 10},
    },
    "EXP105": {
        "name": "Jan Shatabdi",
        "source": "Kolkata", "destination": "Patna",
        "via": ["Asansol", "Dhanbad", "Gaya"],
        "date": "2026-07-14", "departure": "05:00", "arrival": "12:00",
        "price": 450, "coaches": {"SL": 40, "3A": 30, "2A": 20, "1A": 10},
    },
    "EXP106": {
        "name": "Vande Bharat",
        "source": "Delhi", "destination": "Varanasi",
        "via": ["Agra", "Kanpur", "Prayagraj"],
        "date": "2026-07-15", "departure": "06:00", "arrival": "14:00",
        "price": 1800, "coaches": {"SL": 0, "3A": 40, "2A": 30, "1A": 20},
    },
    "EXP107": {
        "name": "Humsafar Express",
        "source": "Mumbai", "destination": "Delhi",
        "via": ["Surat", "Vadodara", "Kota"],
        "date": "2026-07-16", "departure": "11:00", "arrival": "05:00",
        "price": 1350, "coaches": {"SL": 0, "3A": 50, "2A": 30, "1A": 10},
    },
    "EXP108": {
        "name": "Tejas Express",
        "source": "Lucknow", "destination": "Delhi",
        "via": ["Kanpur", "Agra"],
        "date": "2026-07-17", "departure": "06:10", "arrival": "12:25",
        "price": 950, "coaches": {"SL": 0, "3A": 40, "2A": 30, "1A": 10},
    },
}

# ─────────────────────────────────────────────
#  SEAT MAP
# ─────────────────────────────────────────────

seat_map = {}
for tid, t in trains.items():
    seat_map[tid] = {}
    for coach, count in t["coaches"].items():
        seat_map[tid][coach] = {i: None for i in range(1, count + 1)}

# ─────────────────────────────────────────────
#  WAITING QUEUES & PRICE BST
# ─────────────────────────────────────────────

waiting_queues = {tid: Queue() for tid in trains}

price_bst = BST()
for tid, t in trains.items():
    price_bst.insert(t["price"], tid)

# ─────────────────────────────────────────────
#  STATION GRAPH
# ─────────────────────────────────────────────

station_graph = Graph()
connections = [
    ("Delhi",      "Agra",        200),
    ("Agra",       "Kota",        250),
    ("Kota",       "Vadodara",    380),
    ("Vadodara",   "Mumbai",      400),
    ("Vadodara",   "Surat",       130),
    ("Surat",      "Mumbai",      270),
    ("Mumbai",     "Pune",        150),
    ("Pune",       "Goa",         450),
    ("Goa",        "Mangalore",   350),
    ("Mangalore",  "Chennai",     700),
    ("Delhi",      "Kanpur",      440),
    ("Kanpur",     "Allahabad",   200),
    ("Allahabad",  "Asansol",     600),
    ("Allahabad",  "Varanasi",    120),
    ("Kanpur",     "Prayagraj",   200),
    ("Prayagraj",  "Varanasi",    120),
    ("Asansol",    "Kolkata",     230),
    ("Kolkata",    "Dhanbad",     280),
    ("Dhanbad",    "Gaya",        200),
    ("Gaya",       "Patna",       100),
    ("Chennai",    "Vijayawada",  440),
    ("Vijayawada", "Nagpur",      670),
    ("Nagpur",     "Bhopal",      340),
    ("Bhopal",     "Delhi",       600),
    ("Lucknow",    "Kanpur",       80),
    ("Lucknow",    "Delhi",       500),
]
for u, v, km in connections:
    station_graph.add_route(u, v, km)

# ─────────────────────────────────────────────
#  RUNTIME STORES
# ─────────────────────────────────────────────

users           = {}   # {uname: {password, email, phone}}
bookings        = {}   # {bid: {...}}
history_stacks  = {}   # {uname: Stack}
current_user    = [None]
booking_counter = [2000]
pnr_counter     = [5000]
