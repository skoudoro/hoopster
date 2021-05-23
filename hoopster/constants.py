from os.path import join as pjoin

BASE_URL = "https://www.euroleague.net"

API_URL = pjoin(BASE_URL, "euroleague", "api")

# News (XML)
# rssfeed/27/7523.xml

# Player in season (XML)
# https://www.euroleague.net/euroleague/api/players?pcode=ADI&seasoncode=E2019
PLAYERS_URL = pjoin(API_URL, "players")

# Current season teams (XML)
# https://www.euroleague.net/euroleague/api/teams
# Any season teams (XML)
# https://www.euroleague.net/euroleague/api/teams?seasoncode=E2019
TEAMS_URL = pjoin(API_URL, "teams")

# Last 15 Picture galleries (XML)
# https://www.euroleague.net/euroleague/api/gallery
GALLERY_URL = pjoin(API_URL, "gallery")

# The possible seasoncodes are EXXXX for the Euroleague and UXXXX for the Eurocup, being
# XXXX the year that the season starts in.

# RESULTS (XML)
# https://www.euroleague.net/euroleague/api/results
# https://www.euroleague.net/euroleague/api/results?seasoncode=E2019
# https://www.euroleague.net/euroleague/api/results?seasoncode=E2019&gamenumber=12
# Displays all the games played in a specific season, after a specific number of games played in
# that season (in this example, season 2019-20 after 12 games)
RESULTS_URL = pjoin(API_URL, "results")

# SCHEDULE (XML)
# https://www.euroleague.net/euroleague/api/schedules
# Displays all the games scheduled for the current season.
# https://www.euroleague.net/euroleague/api/schedules?seasoncode=E2019
# Displays all the games schedules in a specific season, current or previous, by adding the
# season code at the end of the URL.
# https://www.euroleague.net/euroleague/api/schedules?seasoncode=E2019&gamenumber=12
# Displays all the games scheduled in a specific season, in a specific round in that season.
SCHEDULE_URL = pjoin(API_URL, "schedule")



# STANDINGS (XML)
# https://www.euroleague.net/euroleague/api/standings
# Displays the standings in all the groups of all the stages in the current season.
# https://www.euroleague.net/euroleague/api/standings?seasoncode=E2019
# Displays the standings in all the groups of all the stages in a specific season by adding the
# season code.
# https://www.euroleague.net/euroleague/api/standings?seasoncode=E2019&gamenumber=12
# Displays the standings in all the groups of all the stages in a specific season, in a specific
# round in that season.
STANDINGS_URL = pjoin(API_URL, "standings")

# BOXSCORES (XML)
# https://www.euroleague.net/euroleague/api/games?gamecode=1&seasoncode=E2019
# Displays the complete statistical boxscores of the two teams in a specific game.
BOXSCORES_URL = pjoin(API_URL, "games")

# PLAY-BY-PLAY (JSON)
# https://live.euroleague.net/api/v1/utc/playbyplay?gamecode=103&seasoncode=E2019
# Displays the whole play-by-play list of a specific game.
PLAYBYPLAY_URL = "https://live.euroleague.net/api/v1/utc/playbyplay"
