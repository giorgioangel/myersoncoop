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
import numpy as np
import random
from tqdm import tqdm
from copy import deepcopy
from math import factorial
from itertools import combinations
from utils.helpers import coalition_policy, coalition_stats, default_stats, list_diff
from utils.game import Arena


def connected_components(c):
    # Get connected components of a coalition for this particular graph
    # P1 (index 0) -> stats 1 (index 1,4)
    # P2 (index 5) -> stats 2 (index 6,9)
    # P3 (index 10) -> stats 3 (index 11,14)
    coalition = deepcopy(c)
    players = [0, 5, 10]
    for player in players:
        if player not in coalition:
            for i in range(player + 1, player + 5):
                try:
                    coalition.remove(i)
                except:
                    continue

    policies = [1, 6, 11]
    for policy in policies:
        if policy not in coalition:
            for i in range(policy + 1, policy + 4):
                try:
                    coalition.remove(i)
                except:
                    continue
    return coalition


def get_combinations(players):
    'Get all possible coalitions between players'
    combinations_list = []
    for i in range(0, len(players) + 1):
        oc = combinations(players, i)
        for c in oc:
            combinations_list.append(list(c))
    return combinations_list


def get_combinations_maxsize(players, size):
    'Get all possible coalitions between players'
    combinations_list = []
    for i in range(0, size + 1):
        oc = combinations(players, i)
        for c in oc:
            combinations_list.append(list(c))
    return combinations_list


def get_combinations_size(players, size):
    'Get all coalitions between players of fixed size'
    combinations_list = []
    oc = combinations(players, size)
    for c in oc:
        combinations_list.append(list(c))
    return combinations_list


def get_combinations_for_player(players, player):
    combinations = get_combinations(players)
    with_player = []
    for combination in combinations:
        if player in combination:
            with_player.append(combination)
    return with_player


def rollout(sim_number, coalition_policy, coalition_stats=None, team_b_pol_string='random', address=None):
    #if 'rl' not in coalition_policy and 'rl' != team_b_pol_string:
    game = Arena(team_a_policy_list=deepcopy(coalition_policy), team_a_stats=deepcopy(coalition_stats),
                     team_b_policy_list=[team_b_pol_string for _ in range(3)], address=address)
    rewards = game.simulate_games(n=sim_number)
    rewards = np.array(rewards)
    return np.array(rewards)


def exact_myerson(sim_number, exact_computations, player_stats=None, team_a_pol='random', team_b_pol='random'):
    if not player_stats:
        player_stats = default_stats()

    vertices = 3 * (4 + 1)  # 3 policies, + 4 stats per player
    features = range(vertices)
    '''
    features_label = ['Warrior Max HP', 'Warrior Policy', 'Warrior Attack Power', 'Warrior Healing Power', 'Warrior Control Chance',
                      'Mage Max HP', 'Mage Policy', 'Mage Attack Power', 'Mage Healing Power', 'Mage Control Chance',
                      'Priest Max HP', 'Priest Policy', 'Priest Attack Power', 'Priest Healing Power', 'Priest Control Chance']
                      '''
    #values = np.zeros(vertices)
    values = np.zeros((vertices, sim_number))
    computed_coalitions = {}  # dictionary with computed rollouts
    exact_coalitions = get_combinations_maxsize(features, exact_computations)
    # exact_coalitions = [list(c) for c in set(tuple(c) for c in exact_coalitions)]
    # print('Coalitions ', len(exact_coalitions))
    fv = factorial(vertices)
    print(len(exact_coalitions))
    for c in tqdm(exact_coalitions):
        lc = len(c)
        difference = list_diff(c, list(features))
        cc = connected_components(c)
        rollouts_minus = computed_coalitions.get(str(cc))
        #if rollouts_minus_mean is None:
        if rollouts_minus is None:
            policies_minus = coalition_policy(team_a_pol, cc)
            stats_minus = coalition_stats(cc)
            rollouts_minus = rollout(sim_number=sim_number, coalition_policy=deepcopy(policies_minus),
                                     coalition_stats=deepcopy(stats_minus), team_b_pol_string=team_b_pol)
            #rollouts_minus_mean = np.mean(rollouts_minus)
            #computed_coalitions[str(c)] = rollouts_minus_mean
            computed_coalitions[str(cc)] = rollouts_minus
        for v in difference:
            coalition_with_v = deepcopy(c)
            coalition_with_v.append(v)
            coalition_with_v = connected_components(coalition_with_v)
            rollouts_plus = computed_coalitions.get(str(coalition_with_v))
            if rollouts_plus is None:
                if len(list_diff(c, coalition_with_v)) > 0:
                    policies_plus = coalition_policy(team_a_pol, coalition_with_v)
                    stats_plus = coalition_stats(coalition_with_v)
                    rollouts_plus = rollout(sim_number=sim_number, coalition_policy=deepcopy(policies_plus),
                                            coalition_stats=deepcopy(stats_plus), team_b_pol_string=team_b_pol)
                    computed_coalitions[str(coalition_with_v)] = rollouts_plus
                else:
                    computed_coalitions[str(coalition_with_v)] = rollouts_minus
                    rollouts_plus = rollouts_minus
            values[v] += factorial(lc) * factorial(vertices - lc - 1) / fv * (rollouts_plus - rollouts_minus)
        '''
        ld = len(difference)
        difference = connected_components(difference)
        #rollouts_diff_mean = computed_coalitions.get(str(difference))
        rollouts_diff = computed_coalitions.get(str(difference))
        #if rollouts_diff_mean is None:
        if rollouts_diff is None:
            policies_diff = coalition_policy(team_a_pol, difference)
            stats_diff = coalition_stats(difference)
            rollouts_diff = rollout(sim_number=sim_number, coalition_policy=deepcopy(policies_diff),
                                    coalition_stats=deepcopy(stats_diff), team_b_pol_string=team_b_pol)
            #rollouts_diff_mean = np.mean(rollouts_diff)
            #computed_coalitions[str(difference)] = rollouts_diff_mean
            computed_coalitions[str(difference)] = rollouts_diff
        for v in difference:
            coalition_without_v = deepcopy(difference)
            try:
                coalition_without_v.remove(v)
            except:
                continue
            coalition_without_v = connected_components(coalition_without_v)
            #rollouts_diffout_mean = computed_coalitions.get(str(coalition_without_v))
            rollouts_diffout = computed_coalitions.get(str(coalition_without_v))
            #if rollouts_diffout_mean is None:
            if rollouts_diffout is None:
                if len(list_diff(difference, coalition_without_v)) > 0:
                    policies_diffout = coalition_policy(team_a_pol, coalition_without_v)
                    stats_diffout = coalition_stats(coalition_without_v)
                    rollouts_diffout = rollout(sim_number=sim_number, coalition_policy=deepcopy(policies_diffout),
                                               coalition_stats=deepcopy(stats_diffout), team_b_pol_string=team_b_pol)
                    #rollouts_diffout_mean = np.mean(rollouts_diffout)
                    #computed_coalitions[str(coalition_without_v)] = rollouts_diffout_mean
                    computed_coalitions[str(coalition_without_v)] = rollouts_diffout
                else:
                    #rollouts_diffout_mean = rollouts_diff_mean
                    computed_coalitions[str(coalition_without_v)] = rollouts_diff
                    rollouts_diffout = rollouts_diff
            #values[v] += factorial(ld - 1) * factorial(vertices - ld) / fv * (rollouts_diff_mean - rollouts_diffout_mean)
            values[v] += factorial(ld - 1) * factorial(vertices - ld) / fv * (
                        rollouts_diff - rollouts_diffout)
    '''
    np.savez_compressed('exact_myerson_a'+team_a_pol+'_b'+team_b_pol+'.npz', v=values, allow_pickle=True)
    values = np.mean(values, axis=1)
    print(np.sum(values))
    return values


def exact_shapley(sim_number, exact_computations, player_stats=None,  team_a_pol='random', team_b_pol='random'):
    if not player_stats:
        player_stats = default_stats()

    vertices = 3 * (4 + 1)  # 3 policies, + 4 stats per player
    features = range(vertices)
    '''
    features_label = ['Warrior Max HP', 'Warrior Policy', 'Warrior Attack Power', 'Warrior Healing Power', 'Warrior Control Chance',
                      'Mage Max HP', 'Mage Policy', 'Mage Attack Power', 'Mage Healing Power', 'Mage Control Chance',
                      'Priest Max HP', 'Priest Policy', 'Priest Attack Power', 'Priest Healing Power', 'Priest Control Chance']
                      '''
    # values = np.zeros(vertices)
    values = np.zeros((vertices, sim_number))
    computed_coalitions = {}  # dictionary with computed rollouts
    exact_coalitions = get_combinations_maxsize(features, exact_computations)
    # exact_coalitions = [list(c) for c in set(tuple(c) for c in exact_coalitions)]
    # print('Coalitions ', len(exact_coalitions))
    fv = factorial(vertices)
    print(len(exact_coalitions))
    for c in tqdm(exact_coalitions):
        lc = len(c)
        difference = list_diff(c, list(features))
        #c = connected_components(c)
        #rollouts_minus_mean = computed_coalitions.get(str(c))
        rollouts_minus = computed_coalitions.get(str(c))
        #if rollouts_minus_mean is None:
        if rollouts_minus is None:
            policies_minus = coalition_policy(team_a_pol, c)
            stats_minus = coalition_stats(c)
            rollouts_minus = rollout(sim_number=sim_number, coalition_policy=deepcopy(policies_minus),
                                     coalition_stats=deepcopy(stats_minus), team_b_pol_string=team_b_pol)
            #rollouts_minus_mean = np.mean(rollouts_minus)
            #computed_coalitions[str(c)] = rollouts_minus_mean
            computed_coalitions[str(c)] = rollouts_minus
        for v in difference:
            coalition_with_v = deepcopy(c)
            coalition_with_v.append(v)
            #coalition_with_v = connected_components(coalition_with_v)
            #rollouts_plus_mean = computed_coalitions.get(str(coalition_with_v))
            rollouts_plus = computed_coalitions.get(str(coalition_with_v))
            #if rollouts_plus_mean is None:
            if rollouts_plus is None:
                if len(list_diff(c, coalition_with_v)) > 0:
                    policies_plus = coalition_policy(team_a_pol, coalition_with_v)
                    stats_plus = coalition_stats(coalition_with_v)
                    rollouts_plus = rollout(sim_number=sim_number, coalition_policy=deepcopy(policies_plus),
                                            coalition_stats=deepcopy(stats_plus), team_b_pol_string=team_b_pol)
                    #rollouts_plus_mean = np.mean(rollouts_plus)
                    #computed_coalitions[str(coalition_with_v)] = rollouts_plus_mean
                    computed_coalitions[str(coalition_with_v)] = rollouts_plus
                else:
                    #rollouts_plus_mean = rollouts_minus_mean
                    computed_coalitions[str(coalition_with_v)] = rollouts_minus
                    rollouts_plus = rollouts_minus
            values[v] += factorial(lc) * factorial(vertices - lc - 1) / fv * (rollouts_plus - rollouts_minus)
        '''
        ld = len(difference)
        #difference = connected_components(difference)
        #rollouts_diff_mean = computed_coalitions.get(str(difference))
        rollouts_diff = computed_coalitions.get(str(difference))
        #if rollouts_diff_mean is None:
        if rollouts_diff is None:
            policies_diff = coalition_policy(team_a_pol, difference)
            stats_diff = coalition_stats(difference)
            rollouts_diff = rollout(sim_number=sim_number, coalition_policy=deepcopy(policies_diff),
                                            coalition_stats=deepcopy(stats_diff), team_b_pol_string=team_b_pol)
            #rollouts_diff_mean = np.mean(rollouts_diff)
            #computed_coalitions[str(difference)] = rollouts_diff_mean
            computed_coalitions[str(difference)] = rollouts_diff
        for v in difference:
            coalition_without_v = deepcopy(difference)
            try:
                coalition_without_v.remove(v)
            except:
                continue
            #coalition_without_v = connected_components(coalition_without_v)
            #rollouts_diffout_mean = computed_coalitions.get(str(coalition_without_v))
            rollouts_diffout = computed_coalitions.get(str(coalition_without_v))
            #if rollouts_diffout_mean is None:
            if rollouts_diffout is None:
                if len(list_diff(difference, coalition_without_v)) > 0:
                    policies_diffout = coalition_policy(team_a_pol, coalition_without_v)
                    stats_diffout = coalition_stats(coalition_without_v)
                    rollouts_diffout = rollout(sim_number=sim_number, coalition_policy=deepcopy(policies_diffout),
                                                       coalition_stats=deepcopy(stats_diffout), team_b_pol_string=team_b_pol)
                    #rollouts_diffout_mean = np.mean(rollouts_diffout)
                    #computed_coalitions[str(coalition_without_v)] = rollouts_diffout_mean
                    computed_coalitions[str(coalition_without_v)] = rollouts_diffout
                else:
                    #rollouts_diffout_mean = rollouts_diff_mean
                    computed_coalitions[str(coalition_without_v)] = rollouts_diff
                    rollouts_diffout = rollouts_diff
            #values[v] += factorial(ld - 1) * factorial(vertices - ld) / fv * (rollouts_diff_mean - rollouts_diffout_mean)
            values[v] += factorial(ld - 1) * factorial(vertices - ld) / fv * (rollouts_diff - rollouts_diffout)
    '''
    np.savez_compressed('exact_shapley_a' + team_a_pol + '_b' + team_b_pol + '.npz', v=values, allow_pickle=True)
    values = np.mean(values, axis=1)
    print(np.sum(values))
    return values