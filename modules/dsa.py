"""
dsa.py — All Data Structures used in the project

  • Linked List Node
  • Queue  (Linked List)   → Waiting list
  • Stack                  → Booking history / Undo
  • BST                    → Train prices (Inorder/Preorder/Postorder)
  • Graph (Adj List)       → Station network (BFS + DFS)
"""

from collections import deque


# ─────────────────────────────────────────────
#  LINKED LIST NODE
# ─────────────────────────────────────────────

class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


# ─────────────────────────────────────────────
#  QUEUE  (Linked List)
# ─────────────────────────────────────────────

class Queue:
    def __init__(self):
        self.front = self.rear = None
        self.size = 0

    def enqueue(self, data):
        node = ListNode(data)
        if self.rear:
            self.rear.next = node
        self.rear = node
        if not self.front:
            self.front = node
        self.size += 1

    def dequeue(self):
        if not self.front:
            return None
        data = self.front.data
        self.front = self.front.next
        if not self.front:
            self.rear = None
        self.size -= 1
        return data

    def is_empty(self):
        return self.front is None

    def to_list(self):
        result, cur = [], self.front
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result


# ─────────────────────────────────────────────
#  STACK
# ─────────────────────────────────────────────

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):   self.items.append(item)
    def pop(self):          return self.items.pop() if self.items else None
    def peek(self):         return self.items[-1] if self.items else None
    def is_empty(self):     return len(self.items) == 0
    def all(self):          return list(reversed(self.items))


# ─────────────────────────────────────────────
#  BINARY SEARCH TREE  (by train price)
# ─────────────────────────────────────────────

class BSTNode:
    def __init__(self, price, train_id):
        self.price    = price
        self.train_id = train_id
        self.left     = None
        self.right    = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, price, train_id):
        self.root = self._insert(self.root, price, train_id)

    def _insert(self, node, price, train_id):
        if not node:
            return BSTNode(price, train_id)
        if price < node.price:
            node.left  = self._insert(node.left,  price, train_id)
        else:
            node.right = self._insert(node.right, price, train_id)
        return node

    def inorder(self, node=None, first=True):
        if first: node = self.root
        if not node: return []
        return (self.inorder(node.left, False) +
                [(node.price, node.train_id)] +
                self.inorder(node.right, False))

    def preorder(self, node=None, first=True):
        if first: node = self.root
        if not node: return []
        return ([(node.price, node.train_id)] +
                self.preorder(node.left, False) +
                self.preorder(node.right, False))

    def postorder(self, node=None, first=True):
        if first: node = self.root
        if not node: return []
        return (self.postorder(node.left, False) +
                self.postorder(node.right, False) +
                [(node.price, node.train_id)])

    def search_range(self, lo, hi, node=None, first=True):
        if first: node = self.root
        if not node: return []
        result = []
        if lo < node.price:
            result += self.search_range(lo, hi, node.left, False)
        if lo <= node.price <= hi:
            result.append((node.price, node.train_id))
        if hi > node.price:
            result += self.search_range(lo, hi, node.right, False)
        return result


# ─────────────────────────────────────────────
#  GRAPH  (Adjacency List) — Station Network
# ─────────────────────────────────────────────

class Graph:
    def __init__(self):
        self.adj = {}

    def add_station(self, s):
        if s not in self.adj:
            self.adj[s] = []

    def add_route(self, u, v, km):
        self.add_station(u)
        self.add_station(v)
        self.adj[u].append((v, km))
        self.adj[v].append((u, km))

    def bfs_path(self, start, end):
        if start not in self.adj or end not in self.adj:
            return None
        visited = {start: None}
        q = deque([start])
        while q:
            node = q.popleft()
            if node == end:
                path = []
                while node:
                    path.append(node)
                    node = visited[node]
                return list(reversed(path))
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    visited[neighbor] = node
                    q.append(neighbor)
        return None

    def dfs_all_paths(self, start, end, visited=None, path=None):
        if visited is None: visited = set()
        if path is None:    path    = []
        visited.add(start)
        path = path + [start]
        if start == end:
            return [path]
        paths = []
        for neighbor, _ in self.adj.get(start, []):
            if neighbor not in visited:
                paths += self.dfs_all_paths(neighbor, end, visited.copy(), path)
        return paths

    def display(self):
        from utils.helpers import sep
        print("\n  Station Network (Adjacency List):")
        sep("-")
        for station, neighbors in self.adj.items():
            conn = ", ".join(f"{n}({km}km)" for n, km in neighbors)
            print(f"  {station:14} → {conn}")


# ─────────────────────────────────────────────
#  BINARY SEARCH  (on sorted train ID list)
# ─────────────────────────────────────────────

def binary_search_train(sorted_ids, target):
    lo, hi = 0, len(sorted_ids) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_ids[mid] == target:
            return mid
        elif sorted_ids[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
