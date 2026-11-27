from datetime import datetime

class PollingService:

    NO_GAME_INTERVAL = 1800
    FUTURE_GAME_INTERVAL = 60
    PREGAME_INTERVAL = 5
    LIVE_INTERVAL = 1
    INTERMISSION_INTERVAL = 15
    COMPLETED_INTERVAL = 1800
    DEFAULT_INTERVAL = 60
    ERROR_INTERVAL = 30

    def get_poll_interval(self, game, now=None):

        if game is None:
            return self.NO_GAME_INTERVAL

        state = game.get("gameState")

        if state in ("LIVE", "CRIT"):
            if game.get("clock", {}).get("inIntermission"):
                return self.INTERMISSION_INTERVAL
            else:
                return self.LIVE_INTERVAL

        if state == "PRE":
            return self.PREGAME_INTERVAL

        if state in ("FINAL", "OFF"):
            return self.COMPLETED_INTERVAL

        return self.DEFAULT_INTERVAL