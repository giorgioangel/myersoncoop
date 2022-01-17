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


class Team:
    def __init__(self, stats_list=None, policy_list=['random' for _ in range(3)]):
        if not stats_list:
            stats_list = [default_stats() for _ in range(3)]
        # initializing roles in the team
        self.players = [Warrior(stats=stats_list[0], policy=policy_list[0]), Mage(stats=stats_list[1],
                                                                                  policy=policy_list[1]),
                        Priest(stats=stats_list[2], policy=policy_list[2])]

    def check_gameover(self):
        return (not self.players[0].alive) and (not self.players[1].alive) and (not self.players[2].alive)

    def act(self, enemies):
        for idx in range(len(self.players)):
            self.players, enemies = self.players[idx].act(self.players, enemies)
            # control elapses after 1 turn
            self.players[idx].awake = True
        return enemies
