""" """
from functools import partial, update_wrapper
import hoopster.elb as elb

competition_name = "EuroCup"
competition_code = "U"

season_records = partial(elb.season_records, competition_code=competition_code)
update_wrapper(season_records, elb.season_records)

game_records = partial(elb.game_records, competition_code=competition_code)
update_wrapper(game_records, elb.game_records)

player_highs = partial(elb.player_highs, competition_code=competition_code)
update_wrapper(player_highs, elb.player_highs)

season_records = partial(elb.season_records, competition_code=competition_code)
update_wrapper(season_records, elb.season_records)

latest_team_videos = elb.latest_team_videos

info = partial(elb.competition, competition_code=competition_code)
update_wrapper(info, elb.competition)