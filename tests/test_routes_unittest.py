import os
import tempfile
import unittest

try:
    # Factory pattern: app.py exposes create_app(test_config)
    from app import create_app
    USE_FACTORY = True
except Exception:
    # Global app pattern: app.py exposes `app`
    from app import app as global_app
    USE_FACTORY = False


class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if USE_FACTORY:
            # Try to pass a test config the app can understand
            cls.temp_db = tempfile.NamedTemporaryFile(delete=False)
            cls.app = create_app({
                "TESTING": True,
                # If you use SQLAlchemy, uncomment one of these:
                # "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                # or file-backed:
                # "SQLALCHEMY_DATABASE_URI": f"sqlite:///{cls.temp_db.name}",
                "WTF_CSRF_ENABLED": False,  # if using Flask-WTF
            })
        else:
            global global_app
            global_app.config.update(
                TESTING=True,
                WTF_CSRF_ENABLED=False,
                # "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            )
            cls.app = global_app

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        if USE_FACTORY:
            try:
                os.unlink(cls.temp_db.name)
            except Exception:
                pass

    def test_home_page_200(self):
        """GET / should return 200 and show app name or heading text"""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        # Adjust this assert to a string you actually render on '/'
        self.assertTrue(
            any(key in res.get_data(as_text=True)
                for key in ["BudgetBuddy", "Budget Buddy", "Welcome"]),
            "Home page does not contain expected heading"
        )

    def test_static_assets_ok(self):
        """(Optional) If you serve static assets, ensure server runs without error"""
        # Only if you have a known static file; otherwise skip.
        # res = self.client.get("/static/styles.css")
        # self.assertIn(res.status_code, (200, 304))
        pass
