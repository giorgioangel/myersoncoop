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
import numpy as np
from utils.helpers import default_stats, get_alive_players


class Role:
    'General role class'
    def __init__(self, stats=None, policy='random'):
        if stats:
            self.stats = stats
        else:
            self.stats = default_stats()

        self.policy = policy

        self.awake = True

        self.alive = True
        if self.stats['current hp'] == 0:
            self.alive = False


class Priest(Role):
    'Priest class definition'
    def __init__(self, stats=None, policy='random'):
        super().__init__(stats=stats, policy=policy)
        self.role = 'priest'

    def heal(self, target):
        temp_hp = target.stats['current hp'] + self.stats['healing power']
        target.stats['current hp'] = np.clip(temp_hp, 0, target.stats['max hp'])
        return target

    def act(self, team, enemies, target_idx=None):
        if (self.alive is True) and (self.awake is True) and (self.policy != 'nothing'):
            alive_players_idx = get_alive_players(team)
            if len(alive_players_idx) > 0:
                if self.policy == 'random':
                    target_idx = random.choice(alive_players_idx)
                elif self.policy == 'smart':
                    min_hp = np.float('inf')
                    for idx in alive_players_idx:
                        if team[idx].stats['current hp'] < min_hp:
                            min_hp = team[idx].stats['current hp']
                            target_idx = idx
                elif self.policy == 'rl' and target_idx != None:
                    pass
                else:
                    raise ValueError('Incorrect Policy')
                team[target_idx] = self.heal(team[target_idx])
        return team, enemies


class Warrior(Role):
    'Warrior class definiton'
    def __init__(self, stats=None, policy='random'):
        super().__init__(stats=stats, policy=policy)
        self.role = 'warrior'

    def attack(self, target):
        #temp_hp = target.stats['current hp'] - self.stats['attack power']/(1+target.stats['defense'])
        temp_hp = target.stats['current hp'] - self.stats['attack power']
        target.stats['current hp'] = np.clip(temp_hp, 0, target.stats['max hp'])
        if target.stats['current hp'] == 0:
            target.alive = False
        return target

    def act(self, team, enemies, target_idx=None):
        if (self.alive is True) and (self.awake is True) and (self.policy != 'nothing'):
            alive_players_idx = get_alive_players(enemies.players)
            if len(alive_players_idx) > 0:
                if self.policy == 'random':
                    target_idx = random.choice(alive_players_idx)
                elif self.policy == 'smart':
                    alive_roles = [enemies.players[idx].role for idx in alive_players_idx]
                    if 'priest' in alive_roles:
                        target_idx = alive_roles.index('priest')
                    elif 'mage' in alive_roles:
                        target_idx = alive_roles.index('mage')
                    else:
                        target_idx = alive_roles.index('warrior')
                elif self.policy == 'rl' and target_idx != None:
                    pass
                enemies.players[target_idx] = self.attack(enemies.players[target_idx])
        return team, enemies


class Mage(Role):
    'Mage class definition'
    def __init__(self, stats=None, policy='random'):
        super().__init__(stats=stats, policy=policy)
        self.role = 'mage'

    def control(self, target):
        if random.uniform(0, 1) < self.stats['control chance'] * (1. + self.stats['attack power']/20.):
            target.awake = False
        return target

    def act(self, team, enemies, target_idx=None):
        if (self.alive is True) and (self.awake is True) and (self.policy != 'nothing'):
            alive_players_idx = get_alive_players(enemies.players)
            if len(alive_players_idx) > 0:
                if self.policy == 'random':
                    target_idx = random.choice(alive_players_idx)
                elif self.policy == 'smart':
                    alive_roles = [enemies.players[idx].role for idx in alive_players_idx]
                    if 'priest' in alive_roles:
                        target_idx = alive_roles.index('priest')
                    elif 'mage' in alive_roles:
                        target_idx = alive_roles.index('mage')
                    else:
                        target_idx = alive_roles.index('warrior')
                elif self.policy == 'rl' and target_idx != None:
                    pass
                enemies.players[target_idx] = self.control(enemies.players[target_idx])
        return team, enemies






