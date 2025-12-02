from __future__ import annotations

from datetime import date, timedelta
from typing import List

from ..models import Expense
from ..repositories import ExpenseRepository


class ExpenseService:
    def __init__(self, repository: ExpenseRepository) -> None:
        self.repository = repository

    def create_expense(self, payload: dict) -> Expense:
        expense = Expense(
            date=payload["date"],
            description=payload["description"],
            category=payload["category"],
            amount=payload["amount"],
        )
        return self.repository.add(expense)

    def list_expenses(self, sort_by: str = "date") -> List[dict]:
        descending = sort_by == "date"
        expenses = self.repository.list(sort_by, descending)
        return [self._to_dict(expense) for expense in expenses]

    def delete_expense(self, expense_id: int) -> bool:
        return self.repository.delete(expense_id)

    def category_breakdown(self) -> List[dict]:
        breakdown = self.repository.totals_by_category()
        return [
            {"category": entry["category"], "total": round(entry["total"], 2)}
            for entry in breakdown
        ]

    def daily_trend(self, days: int = 7) -> List[dict]:
        days = max(days, 1)
        raw_totals = self.repository.totals_by_day(days)
        totals_map = {entry["date"]: entry["total"] for entry in raw_totals}
        start_date = date.today() - timedelta(days=days - 1)
        trend: List[dict] = []
        for offset in range(days):
            current = start_date + timedelta(days=offset)
            iso = current.isoformat()
            trend.append({"date": iso, "total": round(totals_map.get(iso, 0.0), 2)})
        return trend

    @staticmethod
    def _to_dict(expense: Expense) -> dict:
        return expense.as_dict()

