import unittest
from app import create_app


class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.app.config["WTF_CSRF_ENABLED"] = False
        cls.client = cls.app.test_client()

    def test_home_page_200(self):
        """GET / should return 200 and show app name or heading text"""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        page = res.get_data(as_text=True)

        self.assertIn("BudgetBuddy", page)
        self.assertIn("Add Expense", page)
        self.assertIn("Expense History", page)
