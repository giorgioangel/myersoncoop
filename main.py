#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 Giorgio Angelotti, ANITI and ISAE-SUPAERO
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from utils.myerson import exact_myerson, exact_shapley
from utils.helpers import default_stats
import json
import time


def save_results(values, full, team_a_pol, team_b_pol, t, calc_type='myerson'):
    results = {}
    roles = ['Warrior', 'Mage', 'Priest']
    stats = ['Max HP', 'Policy', 'Attack Power', 'Healing Power', 'Control Chance']

    for i in range(len(roles) * len(stats)):
        results[roles[i//len(stats)]+' '+stats[i % len(stats)]] = values[i]

    results['Time'] = t

    if full == 0:
        with open("hybrid_"+calc_type+"_a"+team_a_pol+"_b"+team_b_pol+"_results.json", "w") as file:
            json.dump(results, file)
    if full == 1:
        with open("exact_"+calc_type+"_a"+team_a_pol+"_b"+team_b_pol+"_results.json", "w") as file:
            json.dump(results, file)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--sim_num', type=int, action='store', dest='sim_num',
                        help='Number of simulations')

    #parser.add_argument('--address', type=str, action='store', dest='address',
                        #help='address')

    parser.add_argument('--mc_num', type=int, action='store', dest='mc_num',
                        help='Number of Monte Carlo samples')

    parser.add_argument('--exact', type=int, action='store', dest='ex',
                        help='Max size of coalition to be exactly computed (size <= ex and size >= features - ex)')

    parser.add_argument('--full', type=int, action='store', dest='full', default=0,
                        help='Full exact? 1 True, 0 False (Default 0)')

    parser.add_argument('--pol_a', type=str, action='store', dest='pol_a',
                        help='Policy type of Team B')

    parser.add_argument('--pol_b', type=str, action='store', dest='pol_b',
                        help='Policy type of Team B')

    params = parser.parse_args()

    # ray.init(address=params.address)
    # stats_distribution = []
    # stats_distribution.append(default_stats())

    # for stats in stats_distribution:
    ## HYBRYD NOT YET IMPLEMENTED FOR POLICY CHANGE
    #if params.full == 0:
    #    start_time = time.time()
    #    meyerson = hybrid_monte_carlo_myerson(sim_number=params.sim_num, meyerson_M=params.mc_num,
    #                                       exact_computations=params.ex, player_stats=default_stats())
    #    print("Hybrid Myerson --- %s seconds ---" % (time.time() - start_time))
    if params.full == 1:
        print("Exact Myerson Calc", end="\n")
        start_time = time.time()
        myerson = exact_myerson(sim_number=params.sim_num, exact_computations=params.ex, player_stats=default_stats(),
                                 team_a_pol=params.pol_a, team_b_pol=params.pol_b)
        end_time = time.time()
        mye_time = end_time - start_time
        print("Exact Myerson --- %s seconds ---" % (mye_time), end="\n\n")
        save_results(myerson, params.full, params.pol_a, params.pol_b, mye_time)

        print("Exact Shapley Calc", end="\n")
        start_time = time.time()
        shapley = exact_shapley(sim_number=params.sim_num, exact_computations=params.ex, player_stats=default_stats(),
                                team_a_pol=params.pol_a, team_b_pol=params.pol_b)
        end_time = time.time()
        shap_time = end_time - start_time
        print("Exact Shapley --- %s seconds ---" % (shap_time), end="\n\n")
        save_results(shapley, params.full, params.pol_a, params.pol_b, shap_time, calc_type="shapley")
    else:
        print("Error - Full should be 0 or 1")