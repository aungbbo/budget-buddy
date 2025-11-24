from __future__ import annotations

from datetime import date

from flask import Blueprint, redirect, render_template, request, url_for

from ..forms import ExpenseForm
from ..services import ExpenseService

CATEGORY_CHOICES = [
    {"value": "housing", "label": "Housing", "color": "#dbeafe"},
    {"value": "utilities", "label": "Utilities", "color": "#ede9fe"},
    {"value": "dining", "label": "Dining", "color": "#fee2e2"},
    {"value": "grocery", "label": "Grocery", "color": "#dcfce7"},
    {"value": "transportation", "label": "Transportation", "color": "#cffafe"},
    {"value": "entertainment", "label": "Entertainment", "color": "#fce7f3"},
    {"value": "shopping", "label": "Shopping", "color": "#fef3c7"},
    {"value": "additional", "label": "Additional", "color": "#fecaca"},
]


def create_expense_blueprint(service: ExpenseService) -> Blueprint:
    bp = Blueprint("dashboard", __name__)

    @bp.route("/", methods=["GET", "POST"])
    @bp.route("/dashboard", methods=["GET", "POST"])
    def dashboard():
        form = ExpenseForm(request.form if request.method == "POST" else None)
        if request.method == "POST" and form.validate():
            service.create_expense(form.to_dto())
            sort = request.args.get("sort", "date")
            return redirect(url_for("dashboard.dashboard", sort=sort))

        sort_by = request.args.get("sort", "date")
        expenses = service.list_expenses(sort_by)
        return render_template(
            "base.html",
            form=form,
            expenses=expenses,
            today=date.today().isoformat(),
            active_sort=sort_by,
            categories=CATEGORY_CHOICES,
            category_color_map={choice["value"]: choice["color"] for choice in CATEGORY_CHOICES},
        )

    return bp

