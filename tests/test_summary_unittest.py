import unittest
from app import create_app


class TestSummary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.app.config["WTF_CSRF_ENABLED"] = False
        cls.client = cls.app.test_client()



    def _add_expense(self, date, description, category, amount):
        # Posts to the same URL the form uses
        return self.client.post(
            "/dashboard?sort=date",
            data={
                "date": date,
                "description": description,
                "category": category,
                "amount": str(amount),
            },
            follow_redirects=True,
        )

    def test_summary_numbers_on_homepage(self):
        """
        Seed some expenses, then check that the 'No expenses yet.' empty state
        goes away, meaning we have at least one row in the history table.
        """

        # Seed a few expenses
        self._add_expense("2025-11-03", "Salary", "additional", 2000)
        self._add_expense("2025-11-03", "Rent", "housing", 800)
        self._add_expense("2025-11-03", "Groceries", "grocery", 100)

        # Load the dashboard again (root path)
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        page = res.get_data(as_text=True)


        # The initial empty-state text should no longer be present
        self.assertNotIn("No expenses yet.", page)


        # And at least one of our descriptions should be on the page
        self.assertIn("Rent", page)
        self.assertIn("Groceries", page)
