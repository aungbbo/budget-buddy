import unittest
from app import create_app


class TestTransactions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.app.config["WTF_CSRF_ENABLED"] = False
        cls.client = cls.app.test_client()

    def test_add_expense_form(self):
        """
        POST /dashboard?sort=date should accept a valid expense
        and return 200 (no crash) and show the dashboard page.
        """
        payload = {
            "date": "2025-11-01",
            "description": "Groceries at Safeway",
            "category": "grocery",
            "amount": "42.50",
        }
        res = self.client.post("/dashboard?sort=date",
                               data=payload,
                               follow_redirects=True)

        # Should not 404/500
        self.assertEqual(res.status_code, 200)
        page = res.get_data(as_text=True)
        # At least confirm we are back on the main dashboard
        self.assertIn("Add Expense", page)
        self.assertIn("Expense History", page)

    def test_reject_negative_amount(self):
        """
        POST with negative amount should not crash the app.
        """
        payload = {
            "date": "2025-11-01",
            "description": "Broken test",
            "category": "additional",
            "amount": "-5",
        }
        res = self.client.post("/dashboard?sort=date",
                               data=payload,
                               follow_redirects=True)

        # At minimum, app should respond successfully (no 404/500)
        self.assertEqual(res.status_code, 200)
        page = res.get_data(as_text=True)

        self.assertIn("Add Expense", page)
