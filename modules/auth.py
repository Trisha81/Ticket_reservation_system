"""
auth.py — User registration, login, logout
"""

from data.data import users, history_stacks, current_user
from modules.dsa import Stack
from utils.helpers import header, pause, sep


def register():
    header("REGISTER NEW USER")
    uname = input("  Username : ").strip()
    if not uname:
        print("  Username cannot be empty."); pause(); return
    if uname in users:
        print("  Username already taken."); pause(); return
    pwd   = input("  Password : ").strip()
    email = input("  Email    : ").strip()
    phone = input("  Phone    : ").strip()
    users[uname] = {"password": pwd, "email": email, "phone": phone}
    history_stacks[uname] = Stack()
    print(f"\n  ✓ Registered successfully! Welcome, {uname}.")
    pause()


def login():
    header("LOGIN")
    uname = input("  Username : ").strip()
    pwd   = input("  Password : ").strip()
    if uname in users and users[uname]["password"] == pwd:
        current_user[0] = uname
        print(f"\n  ✓ Login successful! Welcome back, {uname}.")
        pause()
        return True
    print("  ✗ Invalid credentials.")
    pause()
    return False


def logout():
    print(f"\n  Goodbye, {current_user[0]}! Have a safe journey.")
    current_user[0] = None
    pause()
