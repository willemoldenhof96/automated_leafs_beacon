import json
import subprocess

NHL_API_URL = "https://api-web.nhle.com/v1/score/now"
TEAM_ABBREVIATION = "TOR"


def get_games():
	response = subprocess.check_output([
		"curl",
		"--silent",
		"--show-error",
		"--fail",
		"--location",
		"--max-time", "15",
		NHL_API_URL
	])
	
	data = json.loads(response.decode("utf-8"))
	return data.get("games", [])

	
def get_leafs_game():
	for game in get_games():
		home = game["homeTeam"]["abbrev"]
		away = game["awayTeam"]["abbrev"]
		
		if TEAM_ABBREVIATION in (home, away):
			return game
		
	return None
		
		
if __name__ == "__main__":
	game = get_leafs_game()
	
	if game:
		print(json.dumps(game, indent=4))
	else:
		print("No Leafs games right now.")
		
		