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
class Bio:
    """Object for defining a person bio."""

    career: str = None
    misc: str = None


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


def referees(offset=0, limit=500):
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


def people(offset=0, limit=500, with_bio=True, with_seasons=True):
    """Retrieve all registered people at Euroleague Basketball.

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


def person_profile(person_code, add_seasons=True): #008463 # 003331  #CWC
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
    data['bio'] = bio_res.json()
    return Person(**utils.normalize_keys(data))
