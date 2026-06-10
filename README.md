# 🚂 Indian Railway Ticket Reservation System
### A Terminal-Based DSA Project in Python

---

## 📁 Project Structure

```
train_reservation/
│
├── main.py                  ← Entry point — run this
│
├── data/
│   └── data.py              ← Seed data: trains, stations, global stores
│
├── modules/
│   ├── dsa.py               ← All DSA implementations
│   ├── auth.py              ← Register / Login / Logout
│   ├── booking.py           ← Book, Cancel, PNR, History, Undo
│   ├── search.py            ← All search features + BST traversals
│   └── admin.py             ← Admin panel
│
└── utils/
    └── helpers.py           ← Display helpers, formatters
```

---

## 🧠 Data Structures Used

| DSA | Location | Purpose |
|-----|----------|---------|
| **Dictionary (Hash Map)** | `data.py` | Users, trains, bookings, seat map |
| **Linked List** | `dsa.py → ListNode` | Backbone of Queue |
| **Queue (Linked List)** | `dsa.py → Queue` | Per-train waiting list |
| **Stack** | `dsa.py → Stack` | Booking history + Undo last booking |
| **Binary Search Tree** | `dsa.py → BST` | Trains indexed by price |
| **BST Inorder** | `search.py` | Trains in ascending price |
| **BST Preorder** | `search.py` | Root-first traversal |
| **BST Postorder** | `search.py` | Leaves-first traversal |
| **Graph (Adj List)** | `dsa.py → Graph` | Station network |
| **BFS** | `dsa.py → bfs_path` | Shortest path between stations |
| **DFS** | `dsa.py → dfs_all_paths` | All paths between stations |
| **Linear Search** | `search.py` | Search by name / source / destination |
| **Binary Search** | `dsa.py → binary_search_train` | Search by train ID |

---

## ✨ Features

### User
- Register / Login / Logout
- View all trains with schedule
- Search trains by source/destination, name, ID, or price range
- Visual seat map with `[ ]` / `[X]` display
- 4 coach classes — SL / 3A / 2A / 1A with different fares
- Multi-passenger booking (up to 4)
- PNR generation & live status check
- Ticket cancellation with 25% charge + automatic waiting list allotment
- Payment mode selection (UPI / Card / Net Banking / Wallet)
- Booking history (Stack — most recent first)
- Undo last booking (Stack pop)

### DSA Visualiser (Menu Option 6)
- BST Inorder traversal → trains in ascending price
- BST Preorder traversal → root first
- BST Postorder traversal → leaves first

### Graph (Menu Options 7 & 8)
- View full station network as adjacency list
- BFS shortest path between any two stations
- DFS all possible paths between stations

### Admin (password: `admin123`)
- View all bookings and users
- Add new trains (auto-inserted into BST)
- View waiting lists (Queue)
- Revenue report with per-train breakdown
- Search any booking by PNR

---

## ▶️ How to Run

```bash
# No installations needed — pure Python 3

cd train_reservation
python main.py
```

---

## 🗂️ Sample Trains Preloaded

| ID | Train | Route | Price |
|----|-------|-------|-------|
| EXP101 | Rajdhani Express | Delhi → Mumbai | ₹1500 |
| EXP102 | Shatabdi Express | Mumbai → Chennai | ₹1200 |
| EXP103 | Duronto Express | Delhi → Kolkata | ₹1100 |
| EXP104 | Garib Rath | Chennai → Delhi | ₹800 |
| EXP105 | Jan Shatabdi | Kolkata → Patna | ₹450 |
| EXP106 | Vande Bharat | Delhi → Varanasi | ₹1800 |
| EXP107 | Humsafar Express | Mumbai → Delhi | ₹1350 |
| EXP108 | Tejas Express | Lucknow → Delhi | ₹950 |

---

## 🛠️ Tech Stack
- Language: **Python 3**
- No external libraries required
- Pure terminal / CLI interface
