import json
import unittest

try:
    from app import create_app
    USE_FACTORY = True
except Exception:
    from app import app as global_app
    USE_FACTORY = False



class TestSummary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if USE_FACTORY:
            cls.app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False})
        else:
            global_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
            cls.app = global_app
        cls.client = cls.app.test_client()

    def _add(self, date, cat, amt, typ):
        return self.client.post(
            "/add",
            data={"date": date, "category": cat, "amount": str(amt), "type": typ},
            follow_redirects=True,
        )



    def test_summary_numbers(self):
        # seed
        self._add("2025-11-03", "Salary", 2000, "income")
        self._add("2025-11-03", "Rent", 800, "expense")
        self._add("2025-11-03", "Groceries", 100, "expense")


        # If JSON endpoint:
        # res = self.client.get("/api/summary")
        # data = res.get_json()
        # self.assertAlmostEqual(data["income"], 2000.0)
        # self.assertAlmostEqual(data["expense"], 900.0)
        # self.assertAlmostEqual(data["balance"], 1100.0)


        # Otherwise, assert the rendered page contains totals:
        res = self.client.get("/")
        page = res.get_data(as_text=True)
        for needle in ["2000", "900", "1100"]:
            self.assertIn(needle, page, f"Expected total {needle} not found on page")
