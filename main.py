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
from utils.shapley import hybrid_monte_carlo_meyerson
from utils.helpers import default_stats
import json


def save_results(values):
    results = {}
    roles = ['Warrior', 'Mage', 'Priest']
    stats = ['Max HP', 'Policy', 'Attack Power', 'Healing Power', 'Control Chance']

    for i in range(len(roles) * len(stats)):
        results[roles[i//len(stats)]+' '+stats[i % len(stats)]] = values[i]

    with open("hybrid_results.json", "w") as file:
        json.dump(results, file)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--sim_num', type=int, action='store', dest='sim_num',
                        help='Number of simulations')

    parser.add_argument('--mc_num', type=int, action='store', dest='mc_num',
                        help='Number of Monte Carlo samples')

    parser.add_argument('--exact', type=int, action='store', dest='ex',
                        help='Max size of coalition to be exactly computed (size <= ex and size >= features - ex)')

    params = parser.parse_args()

    # stats_distribution = []
    # stats_distribution.append(default_stats())

    # for stats in stats_distribution:
    meyerson = hybrid_monte_carlo_meyerson(sim_number=params.sim_num, meyerson_M=params.mc_num,
                                           exact_computations=params.ex, player_stats=default_stats())
    save_results(meyerson)
