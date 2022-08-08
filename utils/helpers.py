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
import random


def list_diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

# initialize equal stats
def default_stats():
    # stat_list = ['current hp', 'max hp', 'attack power', 'healing power', 'control chance]
    stats = {}
    stats['current hp'] = 100
    stats['max hp'] = 100
    stats['attack power'] = 10
    stats['healing power'] = 5
    stats['control chance'] = 0.5
    return stats


def random_stats():
    # stat_list = ['current hp', 'max hp', 'attack power', 'healing power', 'control chance]
    stats = {}
    stats['current hp'] = random.randint(10, 100)
    stats['max hp'] = stats['current hp']
    stats['attack power'] = random.randint(1, 20)
    stats['healing power'] = random.randint(1, 20)
    stats['control chance'] = random.uniform(0.1, 1)
    return stats


def coalition_stats(features_list):
    stat_list = [default_stats() for _ in range(3)]
    #min_max_hp = 0
    min_attack_power = 0
    min_healing_power = 0
    min_control_chance = 0

    players_list = []
    if 0 in features_list:
        players_list.append(0)
    if 5 in features_list:
        players_list.append(1)
    if 10 in features_list:
        players_list.append(2)

    for feature in range(15):
        if feature not in features_list:
            if feature == 2:
                stat_list[0]['attack power'] = min_attack_power
            elif feature == 3:
                stat_list[0]['healing power'] = min_healing_power
            elif feature == 4:
                stat_list[0]['control chance'] = min_control_chance

            elif feature == 7:
                stat_list[1]['attack power'] = min_attack_power
            elif feature == 8:
                stat_list[1]['healing power'] = min_healing_power
            elif feature == 9:
                stat_list[1]['control chance'] = min_control_chance

            elif feature == 12:
                stat_list[2]['attack power'] = min_attack_power
            elif feature == 13:
                stat_list[2]['healing power'] = min_healing_power
            elif feature == 14:
                stat_list[2]['control chance'] = min_control_chance

    for i in range(3):
        if i not in players_list:
            stat_list[i]['current hp'] = 0
            stat_list[i]['max hp'] = 0
    return stat_list


def coalition_policy(original, features_list):
    policy_list = ['nothing' for _ in range(3)]

    players_list = []
    if 1 in features_list:
        policy_list[0] = original
    if 6 in features_list:
        policy_list[1] = original
    if 11 in features_list:
        policy_list[2] = original

    return policy_list


def get_alive_players(player_list):
    return [i for i in range(len(player_list)) if player_list[i].alive is True]