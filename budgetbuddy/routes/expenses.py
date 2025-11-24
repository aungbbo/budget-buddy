from __future__ import annotations

from datetime import date

from flask import Blueprint, redirect, render_template, request, url_for

from ..forms import ExpenseForm
from ..services import ExpenseService


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
        )

    return bp

