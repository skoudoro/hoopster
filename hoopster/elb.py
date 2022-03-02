import warnings

import hoopster.client as client
import hoopster.utils as utils
import hoopster.decorators as dec
from lxml import etree
from dataclasses import dataclass


@dataclass(frozen=True)
class Venue:
    code: str
    name: str = None
    capacity: int = None
    address: str = None
    images: dict = None
    active: bool = None
    notes: str = None


@dataclass(frozen=True)
class Country:
    """Object for defining a country."""

    code: str
    name: str = None


@dataclass(frozen=True)
class Competition:
    """Object for defining a competition."""

    code: str
    name: str = None


@dataclass(frozen=True)
class Coach:
    """Object for defining a coach."""

    code: str
    name: str = None

@dataclass(frozen=True)
class Bio:
    """Object for defining a person bio."""

    summary: str = None
    highlights: str = None


@dec.nested_dataclass(frozen=True)
class Referee:
    """Object for defining a referee."""

    code: str
    name: str = None
    alias: str = None
    nationality: str = None
    country: Country = None
    images: dict = None
    active: bool = None

    # def __post_init__(self, nationality, country):
    #     if nationality is None and country is not None:
    #         self.nationality = self.country.code
    #     elif nationality is not None and country is None:
    #         self.country = Country(code=self.nationality)


@dec.nested_dataclass(frozen=True)
class Person:
    """Object for defining a person."""

    code: str
    name: str = None
    alias: str = None
    alias_raw: str = None
    passport_name: str = None
    passport_surname: str = None
    jersey_name: str = None
    abbreviated_name: str = None
    country: Country = None
    height: int = None
    weight: int = None
    birth_date: str = None
    birth_country: Country = None
    twitter_account: str = None
    images: dict = None
    bio: Bio = None


@dec.nested_dataclass(frozen=True)
class Team:
    """Object for defining a team."""

    code: str
    name: str = None
    abbreviated_name: str = None
    alias: str = None
    is_virtual: bool = False
    country: Country = None
    address: str = None
    website: str = None
    tickets_url: str = None
    twitter_account: str = None
    tv_code: str = None
    venue: Venue = None
    venue_backup: Venue = None
    national_competition_code: str = None
    city: str = None
    president: str = None
    phone: str = None
    images: dict = None


@dataclass(frozen=True)
class GameRecord:
    category_code: str
    category_name: str = None
    value: int = None
    opponent_team_name: str = None
    season_code: str = None
    game_code: int = None
    phase_type: str = None
    game_date: str = None
    season_year: int = None


@dataclass(frozen=True)
class Video:
    code: str = None
    provider: str = None
    title: str = None


@dataclass(frozen=True)
class Season:
    name: str = None
    code: str = None
    alias: str = None
    competition_code: str = None
    year: int = None


@dec.nested_dataclass(frozen=True)
class PlayerSeason:
    person: Person = None
    type: str = None
    type_name: str = None
    active: bool = True
    start_date: str = None
    end_date: str = None
    dorsal: str = None
    dorsal_raw: str = None
    position: int = None
    position_name: str = None
    last_team: str = None
    images: dict = None
    club: Team = None
    season: Season = None

@dataclass(frozen=True)
class Group:
    id: int = None
    order: int = None
    name: str = None
    raw_name: str = None


@dec.nested_dataclass(frozen=True)
class PhaseType:
    code: str = None
    alias: str = None
    name: str = None
    is_group_phase: bool = True


@dec.nested_dataclass(frozen=True)
class GameTeam:
    team: Team = None
    score: int = None
    standings_score: int = None

@dec.nested_dataclass(frozen=True)
class Game:
    game_code: int = None
    season: Season = None
    group: Group = None
    phase_type: PhaseType = None
    round: int = None
    round_alias: str = None
    round_name: str = None
    played: bool = True
    date: str = None
    confirmed_date: bool = True
    confirmed_hour: bool = True
    local_time_zone: int = None
    local_date: str = None
    utc_date: str = None
    local: GameTeam = None
    road: GameTeam = None


@dataclass(frozen=True)
class Stats:
    time_played: int = None
    valuation: int = None
    points: int = None
    field_goals_made2: int = None
    field_goals_attempted2: int = None
    field_goals_made3: int = None
    field_goals_attempted3: int = None
    free_throws_made: int = None
    free_throws_attempted: int = None
    field_goals_made_total: int = None
    field_goals_attempted_total: int = None
    accuracy_made: int = None
    accuracy_attempted: int = None
    total_rebounds: int = None
    defensive_rebounds: int = None
    offensive_rebounds: int = None
    assistances: int = None
    steals: int = None
    turnovers: int = None
    blocks_favour: int = None
    blocks_against: int = None
    fouls_commited: int = None
    fouls_received: int = None
    plus_minus: int = None

    @property
    def effective_field_goal(self):
        """eFG%"""
        return 100*(self.field_goals_made2 +
                    0.5*self.field_goals_made3) / self.field_goals_attempted_total

    @property
    def true_shooting(self):
        """TS% True shooting percentage measures each
        player's shooting efficiency"""
        return  100*self.points/(2*(self.field_goals_attempted_total+0.44*self.free_throws_attempted))

    @property
    def turnover_percentage(self):
        """TOV% (Turnovers percentage)
        Turnover percentage is an estimate of a player's turnovers per 100 individual plays
        """
        return 100*self.turnovers/(self.field_goals_attempted_total+0.44*self.free_throws_attempted+self.assistances+self.turnovers)


@dataclass(frozen=True)
class PlayerStats(Stats):
    dorsal: str = None
    start_five: bool = True
    start_five2: bool = True


@dec.nested_dataclass(frozen=True)
class GamePlayerStats:
    player: PlayerSeason = None
    stats: PlayerStats = None


@dec.nested_dataclass(frozen=True)
class GameTeamStats:
    coach: Coach = None
    players: list[GamePlayerStats] = None
    team: Stats = None
    total: Stats = None

@dec.nested_dataclass(frozen=True)
class GameStats:
    local: GameTeamStats = None
    road: GameTeamStats = None




def _parse_referees(xml_data):
    root = etree.fromstring(bytes(xml_data, encoding='utf-8'))
    referees = [Referee(**dict(r.items())) for r in root.findall('referee')]
    return referees


def referees_1():
    """Get all referees with the API v1. Experimental.
    """
    params = {'version': 1.0, }
    url = client.build_url('referees', **params)
    res = client.get(url)

    return _parse_referees(utils.remove_invalid_characters(res.text))
    # print(res)


def all_referees(year=None, offset=0, limit=500, competition_code=None):
    """Retrieve all registered referees from Euroleague BasketBall .

    Parameters
    ----------
    offset: int, optional
        Offset base zero
    limit: int, optional
        number of items to retrieve

    Returns
    -------
    referees: list
        desired venues

    Notes
    -----
    On June 2021, there is 378 registered referees so no need to use
    limit or offset parameters

    """
    params = {'version': 2.0, 'offset': offset, 'limit': limit}
    url = client.build_url('referees', **params)
    if competition_code and year is None:
        url = client.build_url('competitions', competition_code,
                               'referees', **params)
    elif competition_code and year:
        season_code = f'{competition_code}{year}'
        url = client.build_url('competitions', competition_code,
                               'seasons', season_code,
                               'referees', **params)
    elif competition_code is None and year:
        warnings.warn('No competitions found, returning all referees')

    res = client.get(url)
    return [Referee(**r) for r in res.json()]


def referee(referee_code):
    """Retrieve a referee information.

    Parameters
    ----------
    referee_code: str
        referee id

    Returns
    -------
    referee: dataclass
        all information about the referee
    """
    params = {'version': 2.0}
    url = client.build_url('referees', referee_code, **params)
    res = client.get(url)
    return Referee(**res.json())


def venues(offset=0, limit=500):
    """Retrieve all venues.

    Parameters
    ----------
    offset: int, optional
        Offset base zero
    limit: int, optional
        number of items to retrieve

    Returns
    -------
    venues: list
        desired venues

    Notes
    -----
    On June 2021, there is 482 venues so no need to use limit or offset
    parameters

    """
    params = {'version': 2.0, 'offset': offset, 'limit': limit}
    url = client.build_url('venues', **params)
    res = client.get(url)
    return [Venue(**r) for r in res.json()]


def venue(venue_code):
    """Retrieve a venue information.

    Parameters
    ----------
    venue_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('venues', venue_code, **params)
    res = client.get(url)
    return Venue(**res.json())


def all_profile(offset=0, limit=500, with_bio=True, with_seasons=True):
    """Retrieve all registered profile at Euroleague Basketball.

    Parameters
    ----------
    offset: int, optional
        Offset base zero
    limit: int, optional
        number of items to retrieve

    Returns
    -------
    people: list
        list of registered people based on offset and limit

    Notes
    -----
    On June 2021, there is 13336 registered people

    """
    params = {'version': 2.0, 'offset': offset, 'limit': limit}
    url = client.build_url('people', **params)
    res = client.get(url)
    return [Person(**utils.normalize_keys(r)) for r in res.json()]


def profile(person_code, career_history=True): #008463 # 003331  #CWC
    """Retrieve one registered person from Euroleague BasketBall.

    Parameters
    ----------
    person_code: str
        person id

    Returns
    -------
    person: dataclass
        all information about a person
    """
    params = {'version': 2.0}
    url = client.build_url('people', person_code, **params)
    res = client.get(url)
    data = res.json()
    bio_url = client.build_url('people', person_code, "bio", **params)
    bio_res = client.get(bio_url)
    bio_res = bio_res.json()
    bio_res['summary'] = bio_res.pop('career', None)
    bio_res['highlights'] = bio_res.pop('misc', None)
    data['bio'] = Bio(**bio_res)
    if career_history:
       extra_url = client.build_url('people', person_code, "seasons", **params)
       extra_res = client.get(bio_url)

    return Person(**utils.normalize_keys(data))


def all_teams(offset=0, limit=500):
    """Retrieve all registered teams.

    Parameters
    ----------
    offset: int, optional
        Offset base zero
    limit: int, optional
        number of items to retrieve

    Returns
    -------
    venues: list
        desired venues

    Notes
    -----
    On June 2021, there is 482 venues so no need to use limit or offset
    parameters

    """
    params = {'version': 2.0, 'offset': offset, 'limit': limit}
    url = client.build_url('clubs', **params)
    res = client.get(url)
    return [Team(**r) for r in res.json()]


def team(team_code):
    """Retrieve a team information.

    Parameters
    ----------
    venue_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('clubs', team_code, **params)
    res = client.get(url)
    return Team(**res.json())


def game_records(team_code, competition_code):
    """Retrieve a team competition records per single game.

    Parameters
    ----------
    venue_code: str
        venue id

    Returns
    -------
    game_records: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('clubs', team_code, 'competition', competition_code,
                           'gamerecords', **params)
    res = client.get(url)
    return [GameRecord(**r) for r in res.json()]


def player_highs(team_code, competition_code):
    """Returns team competition player highs.

    Parameters
    ----------
    venue_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('clubs', team_code, 'competition', competition_code,
                           'playerhighs', **params)
    res = client.get(url)
    return [GameRecord(**r) for r in res.json()]


def season_records(team_code, competition_code):
    """Returns team competition player highs.

    Parameters
    ----------
    team_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('clubs', team_code, 'competition', competition_code,
                           'seasonrecords', **params)
    res = client.get(url)
    return [GameRecord(**r) for r in res.json()]


def latest_team_videos(team_code):
    """Returns the latest team videos.

    Parameters
    ----------
    team_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('clubs', team_code, 'videos', **params)
    res = client.get(url)
    return [Video(**r) for r in res.json()]


def all_competitions():
    """Returns all available competitions.

    Parameters
    ----------
    team_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('competitions', **params)
    res = client.get(url)
    return [Competition(**r) for r in res.json()]


def competition(competition_code):
    """Returns all available competitions.

    Parameters
    ----------
    team_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('competitions', competition_code, **params)
    res = client.get(url)
    return Competition(**res.json())


def all_seasons(competition_code):
    """Returns all available competitions.

    Parameters
    ----------
    team_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    params = {'version': 2.0}
    url = client.build_url('competitions', competition_code, 'seasons',
                           **params)
    res = client.get(url)
    return [Season(**r) for r in res.json()]


def season(year, competition_code):
    """Returns all available competitions.

    Parameters
    ----------
    team_code: str
        venue id

    Returns
    -------
    venue: dataclass
        all information about the venue

    """
    season_code = f'{competition_code}{year}'
    params = {'version': 2.0}
    url = client.build_url('competitions', competition_code, 'seasons',
                           season_code, **params)
    res = client.get(url)
    return [Season(**r) for r in res.json()]


def games(competition_code, season_code, only_played=False):
    """Returns all games from a competition season

    Parameters
    ----------
    competition_code : [type]
        [description]
    season_code : [type]
        [description]
    """
    params = {'version': 2.0}
    url = client.build_url('competitions', competition_code, 'seasons',
                           season_code, 'games', **params)
    res = client.get(url)
    games = []
    for game in res.json():
        game["season"] = utils.normalize_keys(game["season"])
        game["group"] = utils.normalize_keys(game["group"])
        game["phase_type"] = utils.normalize_keys(game.pop("phaseType"))
        game["local"] = utils.normalize_keys(game["local"])
        game["road"] = utils.normalize_keys(game["road"])
        game["local"]["team"] = utils.normalize_keys(game["local"].pop("club"))
        game["road"]["team"] = utils.normalize_keys(game["road"].pop("club"))
        # import ipdb; ipdb.set_trace()
        current = Game(**utils.normalize_keys(game))
        if not only_played:
            games += [current, ]
            continue
        if current.played:
            games += [current, ]
    return games


def game_stats(competition_code, season_code, game_code):
    """Returns all games from a competition season

    Parameters
    ----------
    competition_code : [type]
        [description]
    season_code : [type]
        [description]
    """
    params = {'version': 2.0}
    url = client.build_url('competitions', competition_code, 'seasons',
                           season_code, 'games', game_code, 'stats', **params)
    res = client.get(url)
    game = utils.normalize_nested_dict_keys(res.json())
    game = GameStats(**game)
    return game


if __name__ == "__main__":
    g = game_stats('E', 'E2021', 68)
