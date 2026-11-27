import unittest
from polling_service import PollingService

class TestPollingService(unittest.TestCase):

    def setUp(self):
        self.service = PollingService()

    def test_no_game(self):
        self.assertEqual(
            1800,
            self.service.get_poll_interval(None)
        )

    def test_future_game(self):
        self.assertEqual(
            60,
            self.service.get_poll_interval({
                "gameState": "FUT"
            })
        )

    def test_pregame(self):
        self.assertEqual(
            5,
            self.service.get_poll_interval({
                "gameState": "PRE"
            })
        )

    def test_live_game(self):
        self.assertEqual(
            1,
            self.service.get_poll_interval({
                "gameState": "LIVE"
            })
        )

    def test_critical_game(self):
        self.assertEqual(
            1,
            self.service.get_poll_interval({
                "gameState": "CRIT"
            })
        )

    def test_intermission(self):
        self.assertEqual(
            15,
            self.service.get_poll_interval({
                "gameState": "LIVE",
                "clock": {
                    "inIntermission": True
                }
            })
        )

    def test_completed_game(self):
        for state in ("FINAL", "OFF"):
            self.assertEqual(
                1800,
                self.service.get_poll_interval({
                    "gameState": state
                })
            )

    def test_unknown_state(self):
        self.assertEqual(
            60,
            self.service.get_poll_interval({
                "gameState": "UNKNOWN"
            })
        )

    def test_missing_state(self):
        self.assertEqual(
            60,
            self.service.get_poll_interval({})
        )

if __name__ == "__main__":
    unittest.main()