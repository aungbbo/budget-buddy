from __future__ import annotations

import os

from flask import Flask

from .repositories import ExpenseRepository
from .routes import create_expense_blueprint
from .services import ExpenseService


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SECRET_KEY"] = os.environ.get("BUDGETBUDDY_SECRET_KEY", "dev-secret-key")

    repository = ExpenseRepository()
    service = ExpenseService(repository)
    expenses_bp = create_expense_blueprint(service)
    app.register_blueprint(expenses_bp)

    return app
