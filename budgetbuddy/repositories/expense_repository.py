from __future__ import annotations

from typing import Callable, List

from ..models import Expense


class ExpenseRepository:
    """
    Simple in-memory repository. Swap this out for a persistent
    implementation (SQLAlchemy, etc.) without touching the service layer.
    """

    def __init__(self) -> None:
        self._items: List[Expense] = []
        self._next_id = 1

    def add(self, expense: Expense) -> Expense:
        expense.id = self._next_id
        self._next_id += 1
        self._items.append(expense)
        return expense

    def list(self, sort_by: str = "date", descending: bool = False) -> list[Expense]:
        key_map: dict[str, Callable[[Expense], object]] = {
            "date": lambda expense: expense.date,
            "category": lambda expense: expense.category.lower(),
            "amount": lambda expense: expense.amount,
        }
        key_fn = key_map.get(sort_by, key_map["date"])
        return sorted(self._items, key=key_fn, reverse=descending)

