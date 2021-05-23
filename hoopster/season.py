from dataclasses import dataclass

import hoopster.client as client


@dataclass(frozen=True)
class Season:
    year: int

    def teams(self):
        res = requests.request(method='GET', url='https://www.hoopster.net/hoopster/api/teams')
        return 10

    def standings(self):
        return 10

    def schedule(self)