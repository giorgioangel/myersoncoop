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
from copy import deepcopy
from utils.team import Team
import numpy as np
import gym
from utils.helpers import get_alive_players
from itertools import product

class ArenaGym(gym.Env):## team A always starts
    'Define the Arena'
    # TWO TEAMS MADE OF (WARRIOR, MAGE, PRIEST) each fight each other
    # THE WARRIOR CAN ONLY ATTACK
    # THE MAGE CAN ONLY CONTROL
    # THE PRIEST CAN ONLY HEAL
    # EVERY TEAM PERFORM ITS SEQUENCE OF ACTIONS BY TURN, IN THIS ORDER: WARRIOR, MAGE, PRIEST
    def __init__(self, team_a_stats=None, team_b_stats=None, team_a_policy_list=['rl' for _ in range(3)],
                 team_b_policy_list=['random' for _ in range(3)]):
        self.team_a_stats = team_a_stats
        self.team_b_stats = team_b_stats
        self.team_a_policy = team_a_policy_list
        self.team_b_policy = team_b_policy_list
        self.team_a = Team(stats_list=deepcopy(team_a_stats), policy_list=deepcopy(self.team_a_policy))
        self.team_b = Team(stats_list=deepcopy(team_b_stats), policy_list=deepcopy(self.team_b_policy))

        low = np.array(
            [
                #0,
                0,0,0, # 0 hp x3 players of team A, NO x3 0 for sleeping
                0,0,0,  # 0 hp x3 players of team B, NO x3 0 for sleeping
            ],
            dtype=np.float32,
        )

        high = np.array(
            [
                #1000,
                team_a_stats[0]['max hp'], team_a_stats[1]['max hp'], team_a_stats[2]['max hp'],
                team_b_stats[0]['max hp'], team_b_stats[1]['max hp'], team_b_stats[2]['max hp']
            ],
            dtype=np.float32,
        )
        self.observation_space = gym.spaces.Box(low, high, dtype=np.float32)

        self.action_space = gym.spaces.MultiDiscrete((3, 3, 3))
        #self.action_space = gym.spaces.Discrete(3**3)
        #self.action_space = gym.spaces.Box(
        #    np.array([0. for _ in range(9)], dtype=np.float32),
        #    np.array([1. for _ in range(9)], dtype=np.float32),
        #    dtype=np.float32
        #)
        self.steps = 0

        self.state = self.observe_state()
        self.done = False
        self.steps_beyond_done = None
        self.possible_actions_true = [np.array(list(m), dtype=np.int64) for m in product([0, 1, 2], repeat=3)]
        self.possible_actions = np.arange(len(self.possible_actions_true))

    def action_masks(self):
        team_b_alive = get_alive_players(self.team_b.players)
        return [action[0] in team_b_alive for action in self.possible_actions_true]

    def numberToBase(self, n, b):
        if n == 0:
            return [0, 0, 0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        while len(digits) < 3:
            digits.append(0)
        return digits[::-1]

    def actiontolist(self, action):
        warrior_target = np.argmax([action[0], action[1], action[2]])
        mage_target = np.argmax([action[3], action[4], action[5]])
        priest_target = np.argmax([action[6], action[7], action[8]])
        return [warrior_target, mage_target, priest_target]

    def observe_state(self):
        #team_a_current_hp = [self.steps] # 0 for steps
        team_a_current_hp = []  # 0 for steps
        team_a_awake = []
        team_b_current_hp = []
        team_b_awake = []
        for idx in range(len(self.team_a.players)):
            team_a_current_hp.append(self.team_a.players[idx].stats['current hp'])
            #team_a_awake.append(int(self.team_a.players[idx].awake))
            team_b_current_hp.append(self.team_b.players[idx].stats['current hp'])
            #team_b_awake.append(int(self.team_b.players[idx].awake))
        #return np.array(team_a_current_hp+team_a_awake+team_b_current_hp+team_b_awake, dtype=np.float32)
        return np.array(team_a_current_hp+team_b_current_hp, dtype=np.float32)

    def round(self, target_list=None):
        # Team A plays, Check if Team B lost
        self.team_b = self.team_a.act(enemies=self.team_b, target_list=target_list)
        self.steps += 1
        if self.team_b.check_gameover():
            self.done = True
            return 10000  # return 1 if team A won

        # Team B plays, Check if Team A lost
        self.team_a = self.team_b.act(enemies=self.team_a)
        if self.team_a.check_gameover():
            self.done = True
            return -10000  # return -1 if team B won
            #return 0 # return 0 if team A did not win
        reward = 0
        team_a_alive = get_alive_players(self.team_a.players)
        team_b_alive = get_alive_players(self.team_b.players)
        for idx in range(3):
            if target_list[0] in team_b_alive and target_list[1] in team_b_alive and\
                    0 < self.team_a.players[target_list[2]].stats['current hp'] <= 100:
                reward += self.team_a.players[idx].stats['current hp']
                reward -= self.team_b.players[idx].stats['current hp']
        return reward*(4-len(team_b_alive))  # return 0 if they can still play

    def step(self, action):
        #target_list = self.numberToBase(action, 3)
        #target_list = self.actiontolist(action)
        target_list = action
        outcome = self.round(target_list=target_list)
        self.state = self.observe_state()
        if self.steps == 1000:
            self.done = True
        reward = outcome #for the moment because I modified the reward to easen training

        return self.state, reward, self.done, {}

    def reset(self):
        self.team_a = Team(stats_list=deepcopy(self.team_a_stats), policy_list=deepcopy(self.team_a_policy))
        self.team_b = Team(stats_list=deepcopy(self.team_b_stats), policy_list=deepcopy(self.team_b_policy))
        self.done = False
        self.steps = 0
        self.steps_beyond_done = None
        self.state = self.observe_state()
        return self.state


class ArenaGymEval(gym.Env):## team A always starts
    'Define the Arena'
    # TWO TEAMS MADE OF (WARRIOR, MAGE, PRIEST) each fight each other
    # THE WARRIOR CAN ONLY ATTACK
    # THE MAGE CAN ONLY CONTROL
    # THE PRIEST CAN ONLY HEAL
    # EVERY TEAM PERFORM ITS SEQUENCE OF ACTIONS BY TURN, IN THIS ORDER: WARRIOR, MAGE, PRIEST
    def __init__(self, team_a_stats=None, team_b_stats=None, team_a_policy_list=['rl' for _ in range(3)],
                 team_b_policy_list=['random' for _ in range(3)]):
        self.team_a_stats = team_a_stats
        if team_b_stats is None:
            from utils.helpers import default_stats
            team_b_stats = [default_stats() for _ in range(3)]
        self.team_b_stats = team_b_stats
        self.team_a_policy = team_a_policy_list
        self.team_b_policy = team_b_policy_list
        self.team_a = Team(stats_list=deepcopy(team_a_stats), policy_list=deepcopy(self.team_a_policy))
        self.team_b = Team(stats_list=deepcopy(team_b_stats), policy_list=deepcopy(self.team_b_policy))

        low = np.array(
            [
                #0,
                0,0,0, # 0 hp x3 players of team A, NO x3 0 for sleeping
                0,0,0,  # 0 hp x3 players of team B, NO x3 0 for sleeping
            ],
            dtype=np.float32,
        )

        high = np.array(
            [
                #1000,
                team_a_stats[0]['max hp'], team_a_stats[1]['max hp'], team_a_stats[2]['max hp'],
                team_b_stats[0]['max hp'], team_b_stats[1]['max hp'], team_b_stats[2]['max hp']
            ],
            dtype=np.float32,
        )
        self.observation_space = gym.spaces.Box(low, high, dtype=np.float32)

        self.action_space = gym.spaces.MultiDiscrete((3,3,3))
        #self.action_space = gym.spaces.Discrete(3**3)
        #self.action_space = gym.spaces.Box(
        #    np.array([0. for _ in range(9)], dtype=np.float32),
        #    np.array([1. for _ in range(9)], dtype=np.float32),
        #    dtype=np.float32
        #)
        self.steps = 0

        self.state = self.observe_state()
        self.done = False
        self.steps_beyond_done = None
        self.possible_actions_true = [np.array(list(m), dtype=np.int64) for m in product([0, 1, 2], repeat=3)]
        self.possible_actions = np.arange(len(self.possible_actions_true))

    def action_masks(self):
        team_b_alive = get_alive_players(self.team_b.players)
        return [action[0] in team_b_alive for action in self.possible_actions_true]

    def numberToBase(self, n, b):
        if n == 0:
            return [0, 0, 0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        while len(digits) < 3:
            digits.append(0)
        return digits[::-1]

    def actiontolist(self, action):
        warrior_target = np.argmax([action[0], action[1], action[2]])
        mage_target = np.argmax([action[3], action[4], action[5]])
        priest_target = np.argmax([action[6], action[7], action[8]])
        return [warrior_target, mage_target, priest_target]

    def observe_state(self):
        #team_a_current_hp = [self.steps] # 0 for steps
        team_a_current_hp = []  # 0 for steps
        team_a_awake = []
        team_b_current_hp = []
        team_b_awake = []
        for idx in range(len(self.team_a.players)):
            team_a_current_hp.append(self.team_a.players[idx].stats['current hp'])
            #team_a_awake.append(int(self.team_a.players[idx].awake))
            team_b_current_hp.append(self.team_b.players[idx].stats['current hp'])
            #team_b_awake.append(int(self.team_b.players[idx].awake))
        #return np.array(team_a_current_hp+team_a_awake+team_b_current_hp+team_b_awake, dtype=np.float32)
        return np.array(team_a_current_hp+team_b_current_hp, dtype=np.float32)

    def round(self, target_list=None):
        # Team A plays, Check if Team B lost
        self.team_b = self.team_a.act(enemies=self.team_b, target_list=target_list)
        self.steps += 1
        if self.team_b.check_gameover():
            self.done = True
            return 100.*(1./self.steps + 1.)  # return 1 if team A won

        # Team B plays, Check if Team A lost
        self.team_a = self.team_b.act(enemies=self.team_a)
        if self.team_a.check_gameover():
            self.done = True
            return 100.*(-1./self.steps + 1.)  # return -1 if team B won
            #return 0 # return 0 if team A did not win
        return 0.  # return 0 if they can still play

    def step(self, action):
        #target_list = self.numberToBase(action, 3)
        #target_list = self.actiontolist(action)
        target_list = action
        outcome = self.round(target_list=target_list)
        self.state = self.observe_state()
        if self.steps == 1000:
            self.done = True
            reward = 100.
        else:
            reward = outcome

        return self.state, reward, self.done, {}

    def reset(self):
        self.team_a = Team(stats_list=deepcopy(self.team_a_stats), policy_list=deepcopy(self.team_a_policy))
        self.team_b = Team(stats_list=deepcopy(self.team_b_stats), policy_list=deepcopy(self.team_b_policy))
        self.done = False
        self.steps = 0
        self.steps_beyond_done = None
        self.state = self.observe_state()
        return self.state