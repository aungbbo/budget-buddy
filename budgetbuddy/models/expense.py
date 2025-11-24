from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Expense:
    date: date
    description: str
    category: str
    amount: float
    id: int | None = field(default=None)

    # This class represents a single expense entry with details such as date, description,
    # category, amount, and an optional id. Validation is performed in __post_init__ to
    # ensure required fields are non-empty and amount is positive. The as_dict method
    # returns a serializable dictionary representation of the expense.
    def __post_init__(self) -> None:
        self.description = self.description.strip()
        self.category = self.category.strip()
        if not self.description:
            raise ValueError("Description cannot be empty.")
        if not self.category:
            raise ValueError("Category cannot be empty.")
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")

    def as_dict(self) -> dict[str, str | float | int | None]:
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "description": self.description,
            "category": self.category,
            "amount": round(self.amount, 2),
        }

