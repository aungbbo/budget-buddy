from __future__ import annotations

from datetime import date
from typing import Any, Mapping


class ExpenseForm:
    """
    Lightweight form object that performs validation and keeps track of errors.
    Replaces the need for an additional dependency (e.g., WTForms) while
    maintaining testable, object-oriented form handling.
    """

    def __init__(self, form_data: Mapping[str, Any] | None) -> None:
        self._raw = {k: (v or "").strip() for k, v in (form_data or {}).items()}
        self.errors: dict[str, str] = {}
        self.cleaned_data: dict[str, Any] = {}

    @property
    def submitted(self) -> bool:
        return bool(self._raw)

    def validate(self) -> bool:
        self.errors.clear()
        self.cleaned_data.clear()

        self._validate_date()
        self._validate_text_field("description", "Description is required.")
        self._validate_text_field("category", "Category is required.")
        self._validate_amount()

        return not self.errors

    def _validate_date(self) -> None:
        raw_value = self._raw.get("date") or date.today().isoformat()
        try:
            parsed = date.fromisoformat(raw_value)
        except ValueError:
            self.errors["date"] = "Enter a valid date (YYYY-MM-DD)."
            return
        self.cleaned_data["date"] = parsed

    def _validate_text_field(self, field: str, message: str) -> None:
        value = self._raw.get(field, "")
        if not value:
            self.errors[field] = message
        else:
            self.cleaned_data[field] = value

    def _validate_amount(self) -> None:
        raw_value = self._raw.get("amount")
        if not raw_value:
            self.errors["amount"] = "Amount is required."
            return
        try:
            amount = float(raw_value)
        except ValueError:
            self.errors["amount"] = "Amount must be a number."
            return
        if amount <= 0:
            self.errors["amount"] = "Amount must be greater than zero."
            return
        self.cleaned_data["amount"] = amount

    def to_dto(self) -> dict[str, Any]:
        return self.cleaned_data.copy()

    def value(self, field: str, fallback: str = "") -> str:
        if self.submitted:
            return self._raw.get(field, fallback)
        if field == "date":
            return date.today().isoformat()
        return fallback

