import unittest
from goal_detector import GoalDetector

class TestGoalDetector(unittest.TestCase):
	
	def setUp(self):
		self.detector = GoalDetector()
		
	def create_game(
		self,
		leafs_score=0,
		opponent_score=0,
		game_id=1,
		state="LIVE",
		leafs_home=True):

		leafs = {
			"abbrev": "TOR",
			"score": leafs_score
		}
		opponent = {
			"abbrev": "NYI",
			"score": opponent_score
		}
		
		return {
			"id": game_id,
			"gameState": state,
			"homeTeam": leafs if leafs_home else opponent,
			"awayTeam": opponent if leafs_home else leafs
		}
		
	def test_initial_score(self):
		game = self.create_game(2)
		self.assertFalse(self.detector.detect_goal(game))

	def test_leafs_goal(self):
		self.detector.detect_goal(self.create_game(0))
		self.assertTrue(
			self.detector.detect_goal(self.create_game(1))
		)

	def test_duplicate_score(self):
		self.detector.detect_goal(self.create_game(1))
		self.assertFalse(
			self.detector.detect_goal(self.create_game(1))
		)

	def test_opponent_goal(self):
		self.detector.detect_goal(self.create_game(0, 0))
		self.assertFalse(
			self.detector.detect_goal(
				self.create_game(0, 1)
			)
		)

	def test_away_goal(self):
		self.detector.detect_goal(
			self.create_game(0, leafs_home=False)
		)
		self.assertTrue(
			self.detector.detect_goal(
				self.create_game(1, leafs_home=False)
			)
		)

	def test_new_game(self):
		self.detector.detect_goal(self.create_game(3))
		self.assertFalse(
			self.detector.detect_goal(
				self.create_game(0, game_id=2)
			)
		)

	def test_disallowed_goal(self):
		self.detector.detect_goal(self.create_game(1))
		self.assertFalse(
			self.detector.detect_goal(self.create_game(0))
		)
		self.assertTrue(
			self.detector.detect_goal(self.create_game(1))
		)

	def test_overtime_winner(self):
		self.detector.detect_goal(self.create_game(2,2))
		self.assertTrue(
			self.detector.detect_goal(
				self.create_game(3, 2, state="FINAL")
			)
		)

	def test_completed_game(self):
		self.detector.detect_goal(
			self.create_game(2, state="FINAL")
		)
		self.assertFalse(
			self.detector.detect_goal(
				self.create_game(3, state="OFF")
			)
		)

	def test_missing_live_score(self):
		self.detector.detect_goal(self.create_game(2))
		game = self.create_game()
		del game["homeTeam"]["score"]

		self.assertFalse(self.detector.detect_goal(game))
		self.assertFalse(
			self.detector.detect_goal(self.create_game(2))
		)

	def test_pregame_without_score(self):
		game = self.create_game(state="PRE")
		del game["homeTeam"]["score"]
		
		self.detector.detect_goal(game)
		self.assertTrue(
			self.detector.detect_goal(self.create_game(1))
		)

	def test_no_game(self):
		self.assertFalse(self.detector.detect_goal(None))

if __name__ == "__main__":
	unittest.main()