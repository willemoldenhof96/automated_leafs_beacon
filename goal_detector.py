class GoalDetector:

	LIVE_STATES = ("LIVE", "CRIT")
	COMPLETED_STATES = ("FINAL", "OFF")

	def __init__(self):
		self.game_id = None
		self.previous_score = None
		self.previous_state = None
		
	def get_leafs_score(self, game):
		for side in ("homeTeam", "awayTeam"):
			team = game[side]
			
			if team["abbrev"] == "TOR":
				return team.get("score")
				
		return None
		
	def detect_goal(self, game):
		if game is None:
			return False
			
		game_id = game["id"]
		state = game["gameState"]
		current_score = self.get_leafs_score(game)
		
		if current_score is None:
			if state in ("FUT", "PRE"):
				current_score = 0
			else:
				return False
			
		# Establish baseline for a new game
		if self.game_id != game_id:
			self.game_id = game_id
			self.previous_score = current_score
			self.previous_state = state
			return False
			
		goal_scored = current_score > self.previous_score

		is_live = state in self.LIVE_STATES
		was_live = self.previous_state in self.LIVE_STATES
		
		self.previous_score = current_score
		self.previous_state = state
		
		return goal_scored and (
			is_live or (
				was_live and state in self.COMPLETED_STATES
			)
		)		