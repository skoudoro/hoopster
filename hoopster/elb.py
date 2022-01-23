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
    alias: str = None
    is_virtual: bool = True
    country: Country = None
    address: str = None
    website: str = None
    tickets_url: str = None
    twitter_account: str = None
    venue: Venue = None
    venue_backup: Venue = None
    national_competition_code: str = None
    city: str = None
    president: str = None
    phone: str = None
    images: dict = None


@dataclass(frozen=True)
class Season:
    code: str
    name: str = None
    alias: str = None
    competition_code: str = None
    year: int = None
    start_date: str = None
    end_date: str = None
    activation_date: str = None


@dec.nested_dataclass(frozen=True)
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


@dec.nested_dataclass(frozen=True)
class Video:
    code: str = None
    provider: str = None
    title: str = None


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


def all_teams(offset=0, limit=700):
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
    On June 2021, there is 666 teams so no need to use limit or offset
    parameters

    """
    params = {'version': 2.0, 'offset': offset, 'limit': limit}
    url = client.build_url('clubs', **params)
    res = client.get(url)
    teams = []
    for team in res.json():
        team["is_virtual"] = team.pop('isVirtual')
        team["tickets_url"] = team.pop('ticketsUrl')
        team["twitter_account"] = team.pop('twitterAccount')
        team["venue_backup"] = team.pop('venueBackup')
        team["national_competition_code"] = team.pop('nationalCompetitionCode')

        teams.append(Team(**team))
    return teams


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
    current_team = res.json()
    current_team["is_virtual"] = current_team.pop('isVirtual')
    current_team["tickets_url"] = current_team.pop('ticketsUrl')
    current_team["twitter_account"] = current_team.pop('twitterAccount')
    current_team["venue_backup"] = current_team.pop('venueBackup')
    current_team["national_competition_code"] = current_team.pop('nationalCompetitionCode')
    return Team(**current_team)


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
    """Return team competition player highs.

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
    """Return team competition player highs.

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
    """Return the latest team videos.

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
    """Return all available competitions.

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
    """Return all available competitions.

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
    """Return all available competitions.

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
    seasons = []
    for season in res.json():
        season['start_date'] = season.pop('startDate')
        season['end_date'] = season.pop('endDate')
        season['activation_date'] = season.pop('activationDate')
        season['competition_code'] = season.pop('competitionCode')
        seasons.append(Season(**season))
    return seasons


def season(year, competition_code):
    """Return all available competitions.

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
    season = res.json()
    season['start_date'] = season.pop('startDate')
    season['end_date'] = season.pop('endDate')
    season['activation_date'] = season.pop('activationDate')
    season['competition_code'] = season.pop('competitionCode')

    return Season(**season)




