import unittest

try:
    from app import create_app
    USE_FACTORY = True
except Exception:
    from app import app as global_app
    USE_FACTORY = False


class TestTransactions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if USE_FACTORY:
            cls.app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False})
        else:
            global_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
            cls.app = global_app
        cls.client = cls.app.test_client()

    def test_add_expense_form(self):
        """
        POST /add should accept a valid expense and redirect back to list/dashboard.
        Adjust field names ('date','category','amount','type') to match your form.
        """
        payload = {
            "date": "2025-11-01",
            "category": "Groceries",
            "amount": "42.50",
            "type": "expense",   # or what your form expects
        }
        res = self.client.post("/add", data=payload, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        page = res.get_data(as_text=True)
        # Expect to see category or some success cue on the redirected page
        self.assertIn("Groceries", page)

    def test_reject_negative_amount(self):
        """
        POST /add with negative amount should be rejected (flash error or 400).
        Adjust assertion to your error handling (message/status).
        """
        payload = {
            "date": "2025-11-01",
            "category": "Test",
            "amount": "-5",
            "type": "expense",
        }
        res = self.client.post("/add", data=payload, follow_redirects=True)
        # If you raise 400 for invalid data:
        # self.assertEqual(res.status_code, 400)
        # If you flash an error and redirect:
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            any(s in res.get_data(as_text=True) for s in ["Invalid", "must be positive", "Error"]),
            "Expected validation message for negative amount",
        )

    def test_edit_flow(self):
        """
        If you support editing: typically POST /edit/<id> or /edit with hidden id.
        This test assumes you already created at least one item.
        You can seed first by adding, then editing.
        """
        # 1) Create an item
        create_payload = {
            "date": "2025-11-02",
            "category": "Coffee",
            "amount": "4.75",
            "type": "expense",
        }
        self.client.post("/add", data=create_payload, follow_redirects=True)

        # 2) Find the id to edit. If your UI renders an ID, parse it.
        # If you expose an API endpoint, call it; otherwise skip ID check and assume /edit/1 exists.
        # For demonstration:
        edit_id = 1  # Adjust based on storage mechanism

        edit_payload = {
            "date": "2025-11-02",
            "category": "Coffee",
            "amount": "5.00",
            "type": "expense",
        }
        res = self.client.post(f"/edit/{edit_id}", data=edit_payload, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("5.00", res.get_data(as_text=True))
