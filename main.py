import time
import logging

from nhl_service import get_leafs_game
from goal_detector import GoalDetector
from beacon_service import BeaconService
from polling_service import PollingService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    detector = GoalDetector()
    beacon = BeaconService()
    polling = PollingService()

    logger.info("Leafs Goal Beacon service started")

    while True:
        try:
            game = get_leafs_game()

            if game is None:
                logger.info("No Leafs game today")
            else:
                home = game["homeTeam"]
                away = game["awayTeam"]

                logger.info(
                    "%s %s - %s %s | State: %s",
                    away["abbrev"],
                    away.get("score", 0),
                    home.get("score", 0),
                    home["abbrev"],
                    game.get("gameState")
                )

                if detector.detect_goal(game):
                    logger.info("LEAFS GOAL! Activate beacon!")
                    beacon.activate()

            interval = polling.get_poll_interval(game)

            logger.info("Next poll in %s seconds", interval)

            time.sleep(interval)

        except KeyboardInterrupt:
            logger.info("Leafs Goal Beacon service stopped")
            break

        except Exception:
            logger.exception("Error monitoring Leafs game")
            time.sleep(polling.ERROR_INTERVAL)

if __name__ == "__main__":
    main()