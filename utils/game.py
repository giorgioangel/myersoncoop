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
import multiprocessing as mp
from copy import deepcopy
from utils.team import Team


class Arena:
    'Define the Arena'
    # TWO TEAMS MADE OF (WARRIOR, MAGE, PRIEST) each fight each other
    # THE WARRIOR CAN ONLY ATTACK
    # THE MAGE CAN ONLY CONTROL
    # THE PRIEST CAN ONLY HEAL
    # EVERY TEAM PERFORM ITS SEQUENCE OF ACTIONS BY TURN, IN THIS ORDER: WARRIOR, MAGE, PRIEST
    def __init__(self, team_a_stats=None, team_b_stats=None, team_a_policy_list=['random' for _ in range(3)],
                 team_b_policy_list=['random' for _ in range(3)]):
        self.team_a_stats = team_a_stats
        self.team_b_stats = team_b_stats
        self.team_a_policy = team_a_policy_list
        self.team_b_policy = team_b_policy_list
        self.team_a = Team(stats_list=deepcopy(team_a_stats), policy_list=deepcopy(self.team_a_policy))
        self.team_b = Team(stats_list=deepcopy(team_b_stats), policy_list=deepcopy(self.team_b_policy))
        # random starting order
        self.order = random.choice([0, 1])

    def round(self):
        if self.order == 0: # Team A plays first
            # Team A plays, Check if Team B lost
            self.team_b = self.team_a.act(self.team_b)
            if self.team_b.check_gameover():
                return 1  # return 1 if team A won

            # Team B plays, Check if Team A lost
            self.team_a = self.team_b.act(self.team_a)
            if self.team_a.check_gameover():
                return -1  # return -1 if team B won
                #return 0 # return 0 if team A did not win

        else: #team B plays first
            # Team B plays, Check if Team A lost
            self.team_a = self.team_b.act(self.team_a)
            if self.team_a.check_gameover():
                return -1  # return -1 if team B won
                #return 0  # return 0 if team A did not win

            # Team A plays, Check if Team B lost
            self.team_b = self.team_a.act(self.team_b)
            if self.team_b.check_gameover():
                return 1  # return 1 if team A won

        return 0  # return 0 if they can still play

    def play(self):
        self.__init__(team_a_stats=deepcopy(self.team_a_stats), team_b_stats=deepcopy(self.team_b_stats),
                      team_a_policy_list=deepcopy(self.team_a_policy), team_b_policy_list=deepcopy(self.team_b_policy))
        outcome = self.round()
        steps = 1.
        while outcome == 0 and steps < 1000:
            outcome = self.round()
            steps += 1.
        return 100*(outcome/steps + 1.)

    # simulate n games
    def simulate_games(self, n):
        pool = mp.Pool(mp.cpu_count())
        result = pool.starmap_async(self.play, [() for _ in range(n)])
        pool.close()
        pool.join()
        outcomes = result.get()
        return outcomes