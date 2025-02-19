import unittest
from scripts.generate_alerts import generate_alert

class TestAlertGeneration(unittest.TestCase):

    def test_generate_alert(self):
        alert = generate_alert()
        self.assertIsInstance(alert, dict)
        self.assertIn("alert_id", alert)
        self.assertIn("alert_type", alert)
        self.assertIn("timestamp", alert)
        self.assertIn("severity", alert)

if __name__ == '__main__':
    unittest.main()
