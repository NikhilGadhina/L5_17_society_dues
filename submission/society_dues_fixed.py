"""In-memory apartment-society maintenance dues ledger for Lab 5."""

import sqlite3

DB_CONNECTION = sqlite3.connect(":memory:")
DB_CONNECTION.execute(
    "CREATE TABLE dues ("
    "flat TEXT NOT NULL, month TEXT NOT NULL, amount INTEGER NOT NULL, "
    "paid INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (flat, month))"
)


def add_due(flat, month, amount, history=None):
    """Add or replace one monthly due and return the updated history."""
    if amount < 0:
        raise ValueError("amount must be non-negative")
    due_history = [] if history is None else history
    DB_CONNECTION.execute(
        "INSERT INTO dues (flat, month, amount, paid) VALUES (?, ?, ?, 0) "
        "ON CONFLICT(flat, month) DO UPDATE SET "
        "amount = excluded.amount, paid = 0",
        (flat, month, amount),
    )
    due_history.append((flat, month))
    return due_history


def collect(flat, month):
    """Mark a flat's due as paid and return its amount, or None if absent."""
    row = DB_CONNECTION.execute(
        "SELECT amount FROM dues WHERE flat = ? AND month = ?",
        (flat, month),
    ).fetchone()
    if row is None:
        return None
    DB_CONNECTION.execute(
        "UPDATE dues SET paid = 1 WHERE flat = ? AND month = ?",
        (flat, month),
    )
    return row[0]


def calculate_penalty(days_late, daily_fee):
    """Calculate a late fee from non-negative days late and daily fee."""
    if days_late < 0 or daily_fee < 0:
        raise ValueError("days late and daily fee must be non-negative")
    return days_late * daily_fee


def pending():
    """Return flat identifiers with unpaid dues."""
    rows = DB_CONNECTION.execute(
        "SELECT flat FROM dues WHERE paid = 0"
    ).fetchall()
    return [row[0] for row in rows]


def main():
    """Run the sample dues-ledger demonstration."""
    add_due("A-101", "Oct", 2500)
    add_due("A-102", "Oct", 2500)
    print(collect("A-101", "Oct"))
    print(calculate_penalty(50, 2))  # simple daily-rate example
    print(pending())


if __name__ == "__main__":
    main()
