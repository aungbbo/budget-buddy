from __future__ import annotations

from datetime import date
from typing import Iterable, List

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

    @staticmethod
    def _to_dict(expense: Expense) -> dict:
        return expense.as_dict()

