""" """

import hoopster.elb as elb


def test_referees():
    r = elb.referees()
    # print(r)


if __name__ == "__main__":
    # test_referees()
    # pe = elb.people()
    # import ipdb; ipdb.set_trace()
    # print(pe)
    p = elb.person("KRV")
    print(p)
    # # ref = referees()
    # all_ref = referees()
    # print(len(all_ref))
    # ref = referee('OJDN')
    # print(ref)
    # all_venues = venues()
    # print(len(all_venues))
    # print(all_venues[15])
    # # import ipdb; ipdb.set_trace()
    # ven = venue(all_venues[15].code)
    # print(ven)
