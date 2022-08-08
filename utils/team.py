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
from utils.roles import Warrior, Mage, Priest
from utils.helpers import default_stats
import numpy as np

'''
@nb.jit(nopython=True, cache=True, nogil=True)
def _policy_rl(state, w1, b1, w2, b2, w3, b3):
    l1 = np.tanh(w1 @ state + b1)
    l2 = np.tanh(w2 @ l1 + b2)
    l3 = w3 @ l2 + b3
    p0 = l3[:3]
    p1 = l3[3:6]
    p2 = l3[6:]
    return [np.argmax(p0), np.argmax(p1), np.argmax(p2)]
'''

class Team:
    def __init__(self, stats_list=None, policy_list=['random' for _ in range(3)]):
        if not stats_list:
            stats_list = [default_stats() for _ in range(3)]
        # initializing roles in the team
        self.players = [Warrior(stats=stats_list[0], policy=policy_list[0]), Mage(stats=stats_list[1],
                                                                                  policy=policy_list[1]),
                        Priest(stats=stats_list[2], policy=policy_list[2])]

        if 'rl' in policy_list:
            data = np.load('a2c_actor_numpy.npz')
            self.w1 = data['w1']
            self.b1 = data['b1']
            self.w2 = data['w2']
            self.b2 = data['b2']
            self.w3 = data['w3']
            self.b3 = data['b3']
        else:
            self.w1 = None
            self.b1 = None
            self.w2 = None
            self.b2 = None
            self.w3 = None
            self.b3 = None

    def policy_rl(self, state):
        l1 = np.tanh(self.w1 @ state + self.b1)
        l2 = np.tanh(self.w2 @ l1 + self.b2)
        l3 = self.w3 @ l2 + self.b3
        p0 = l3[:3]
        p1 = l3[3:6]
        p2 = l3[6:]
        return [np.argmax(p0), np.argmax(p1), np.argmax(p2)]

    def check_gameover(self):
        return (not self.players[0].alive) and (not self.players[1].alive) and (not self.players[2].alive)

    def act(self, enemies, target_list=None):
        if (target_list is None) and (self.w1 is not None):
            friends_current_hp = []  # 0 for steps
            enemies_current_hp = []
            for idx in range(len(self.players)):
                friends_current_hp.append(self.players[idx].stats['current hp'])
                enemies_current_hp.append(enemies.players[idx].stats['current hp'])
            state = np.array(friends_current_hp + enemies_current_hp, dtype=np.float32)
            target_list = self.policy_rl(state)
            for idx in range(len(self.players)):
                if self.players[idx].policy != 'rl':
                    target_list[idx] = -1

        for idx in range(len(self.players)):
            if (target_list is None) or (target_list[idx] == -1):
                self.players, enemies = self.players[idx].act(self.players, enemies)
            else:
                self.players, enemies = self.players[idx].act(self.players, enemies, int(target_list[idx]))
            # control elapses after 1 turn
            self.players[idx].awake = True

        return enemies