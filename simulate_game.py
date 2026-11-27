import time
import logging

from goal_detector import GoalDetector
from beacon_service import BeaconService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

def simulate_game():
    detector = GoalDetector()
    beacon = BeaconService()

    scores = [
        (0,0),
        (0,1),
        (1,1),
        (1,1),
        (2,1),
        (2,2),
        (3,2),
        (4,2),
        (4,2),
    ]

    for leafs_score, opponent_score in scores:
        game = {
            "id": 12345,
            "gameState": "LIVE",
            "awayTeam": {
                "abbrev": "TOR",
                "score": leafs_score
            },
            "homeTeam": {
                "abbrev": "NYI",
                "score": opponent_score
            }
        }

        logging.info(
            "TOR %s - %s NYI",
            leafs_score,
            opponent_score
        )

        if detector.detect_goal(game):
            logging.info("LEAGS GOAL!")
            beacon.activate()

        time.sleep(2)

    logging.info("Simulation complete")

if __name__ == "__main__":
    simulate_game()