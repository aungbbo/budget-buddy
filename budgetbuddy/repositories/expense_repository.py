from __future__ import annotations

from datetime import date, timedelta

from ..db import db_connection
from ..models import Expense


class ExpenseRepository:
    """
    SQLite-backed repository implementation. Persists expenses using
    the helpers provided in budgetbuddy.db.
    """

    _SORT_COLUMN_MAP: dict[str, str] = {
        "date": "date",
        "category": "category",
        "amount": "amount",
    }

    def add(self, expense: Expense) -> Expense:
        with db_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO expenses (date, description, amount, category)
                VALUES (?, ?, ?, ?)
                """,
                (
                    expense.date.isoformat(),
                    expense.description,
                    expense.amount,
                    expense.category,
                ),
            )
            expense.id = cursor.lastrowid
        return expense

    def list(self, sort_by: str = "date", descending: bool = False) -> list[Expense]:
        column = self._SORT_COLUMN_MAP.get(sort_by, self._SORT_COLUMN_MAP["date"])
        direction = "DESC" if descending else "ASC"
        query = f"""
            SELECT id, date, description, amount, category
            FROM expenses
            ORDER BY {column} {direction}, id ASC
        """
        with db_connection() as conn:
            rows = conn.execute(query).fetchall()
        return [self._row_to_expense(row) for row in rows]

    def delete(self, expense_id: int) -> bool:
        with db_connection() as conn:
            cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            return cursor.rowcount > 0

    def totals_by_category(self) -> list[dict[str, float]]:
        with db_connection() as conn:
            rows = conn.execute(
                """
                SELECT category, SUM(amount) AS total
                FROM expenses
                GROUP BY category
                ORDER BY total DESC
                """
            ).fetchall()
        return [{"category": row["category"], "total": row["total"]} for row in rows]

    def totals_by_day(self, days: int = 7) -> list[dict[str, float]]:
        days = max(days, 1)
        start_date = (date.today() - timedelta(days=days - 1)).isoformat()
        with db_connection() as conn:
            rows = conn.execute(
                """
                SELECT date, SUM(amount) AS total
                FROM expenses
                WHERE date >= ?
                GROUP BY date
                ORDER BY date ASC
                """,
                (start_date,),
            ).fetchall()
        return [{"date": row["date"], "total": row["total"]} for row in rows]

    @staticmethod
    def _row_to_expense(row) -> Expense:
        return Expense(
            id=row["id"],
            date=date.fromisoformat(row["date"]),
            description=row["description"],
            category=row["category"],
            amount=row["amount"],
        )

