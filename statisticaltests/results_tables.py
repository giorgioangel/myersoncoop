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

import json
import numpy as np
import scipy.stats as stats


def round_with_padding(value, round_digits):
    return format(round(value, round_digits), "."+str(round_digits)+"f")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--policy', type=str, action='store', dest='pol_a',
                        help='Pol A')

    params = parser.parse_args()

    pol_a = params.pol_a

    sbrandom = open("exact_shapley_a"+pol_a+"_brandom_results.json")
    mbrandom = open("exact_myerson_a"+pol_a+"_brandom_results.json")
    sbsmart = open("exact_shapley_a"+pol_a+"_bsmart_results.json")
    mbsmart = open("exact_myerson_a"+pol_a+"_bsmart_results.json")
    sbnop = open("exact_shapley_a"+pol_a+"_bnothing_results.json")
    mbnop = open("exact_myerson_a"+pol_a+"_bnothing_results.json")

    dsrandom = json.load(sbrandom)
    dmrandom = json.load(mbrandom)
    dssmart = json.load(sbsmart)
    dmsmart = json.load(mbsmart)
    dsnop = json.load(sbnop)
    dmnop = json.load(mbnop)

    sbrandom.close()
    mbrandom.close()
    sbsmart.close()
    mbsmart.close()
    sbnop.close()
    mbnop.close()

    data = np.load('exact_myerson_a'+pol_a+'_bnothing.npz')
    vmn = data['v']
    data = np.load('exact_myerson_a'+pol_a+'_brandom.npz')
    vmr = data['v']
    data = np.load('exact_myerson_a'+pol_a+'_bsmart.npz')
    vms = data['v']


    data = np.load('exact_shapley_a'+pol_a+'_bnothing.npz')
    vsn = data['v']
    data = np.load('exact_shapley_a'+pol_a+'_brandom.npz')
    vsr = data['v']
    data = np.load('exact_shapley_a'+pol_a+'_bsmart.npz')
    vss = data['v']

    attributes = list(dsrandom.keys())
    zeroes = np.zeros(vsn.shape[1])
    psr = {}
    pmr = {}
    psn = {}
    pmn = {}
    pss = {}
    pms = {}

    for i in range(vsr.shape[0]):
        if np.all(vsr[i] != 0):
            res, pv = stats.mannwhitneyu(vsr[i], zeroes)
            if pv < 0.001:
                psr[attributes[i]] = "${}^{***}$"
            elif pv < 0.01:
                psr[attributes[i]] = "${}^{**}$"
            elif pv < 0.05:
                psr[attributes[i]] = "${}^{*}$"
            else:
                psr[attributes[i]] = ""
        else:
            psr[attributes[i]] = ""

        if np.all(vmr[i] != 0):
            res, pv = stats.mannwhitneyu(vmr[i], zeroes)
            if pv < 0.001:
                pmr[attributes[i]] = "${}^{***}$"
            elif pv < 0.01:
                pmr[attributes[i]] = "${}^{**}$"
            elif pv < 0.05:
                pmr[attributes[i]] = "${}^{*}$"
            else:
                pmr[attributes[i]] = ""
        else:
            pmr[attributes[i]] = ""

        if np.all(vsn[i]!=0):
            res, pv = stats.mannwhitneyu(vsn[i], zeroes)
            if pv < 0.001:
                psn[attributes[i]] = "${}^{***}$"
            elif pv < 0.01:
                psn[attributes[i]] = "${}^{**}$"
            elif pv < 0.05:
                psn[attributes[i]] = "${}^{*}$"
            else:
                psn[attributes[i]] = ""
        else:
            psn[attributes[i]] = ""

        if np.all(vmn[i] != 0):
            res, pv = stats.mannwhitneyu(vmn[i], zeroes)
            if pv < 0.001:
                pmn[attributes[i]] = "${}^{***}$"
            elif pv < 0.01:
                pmn[attributes[i]] = "${}^{**}$"
            elif pv < 0.05:
                pmn[attributes[i]] = "${}^{*}$"
            else:
                pmn[attributes[i]] = ""
        else:
            pmn[attributes[i]] = ""

        if np.all(vss[i] != 0):
            res, pv = stats.mannwhitneyu(vss[i], zeroes)
            if pv < 0.001:
                pss[attributes[i]] = "${}^{***}$"
            elif pv < 0.01:
                pss[attributes[i]] = "${}^{**}$"
            elif pv < 0.05:
                pss[attributes[i]] = "${}^{*}$"
            else:
                pss[attributes[i]] = ""
        else:
            pss[attributes[i]] = ""

        if np.all(vms[i] != 0):
            res, pv = stats.mannwhitneyu(vms[i], zeroes)
            if pv < 0.001:
                pms[attributes[i]] = "${}^{***}$"
            elif pv < 0.01:
                pms[attributes[i]] = "${}^{**}$"
            elif pv < 0.05:
                pms[attributes[i]] = "${}^{*}$"
            else:
                pms[attributes[i]] = ""
        else:
            pms[attributes[i]] = ""

    with open(pol_a+".tex", "w") as file:
        file.write("\\begin{tabular}{lllllll}\n")
        file.write("&\multicolumn{2}{c}{"+pol_a.title()+" vs Random}&\multicolumn{2}{c}{"+pol_a.title()+" vs Smart}&\multicolumn{2}{c}{"+pol_a.title()+" vs No-Op}\\\\\n")
        file.write("\\textbf{Feature}         & \\textit{\\textbf{Shapley}} & \\textit{\\textbf{Myerson}}& \\textit{\\textbf{Shapley}} & \\textit{\\textbf{Myerson}}& \\textit{\\textbf{Shapley}} & \\textit{\\textbf{Myerson}} \\\\\n")
        file.write("\hline\n")
        file.write("&                           & & & & &                          \\\\\n")
        file.write("\\textbf{Agent: Warrior }        &                           &                           \\\\\n")
        file.write("\\textit{MaxHealthPoints} & "+round_with_padding(dsrandom['Warrior Max HP'], 2)+psr['Warrior Max HP']+"                   & "+round_with_padding(dmrandom['Warrior Max HP'], 2)+pmr['Warrior Max HP']+" & "+round_with_padding(dssmart['Warrior Max HP'], 2)+pss['Warrior Max HP']+" &  "+round_with_padding(dmsmart['Warrior Max HP'], 2)+pms['Warrior Max HP']+" & "+round_with_padding(dsnop['Warrior Max HP'], 2)+psn['Warrior Max HP']+"  & "+round_with_padding(dmnop['Warrior Max HP'], 2)+pmn['Warrior Max HP']+"                \\\\\n")
        file.write("\\textit{Policy}     & "+round_with_padding(dsrandom['Warrior Policy'], 2)+psr['Warrior Policy']+"                    & "+round_with_padding(dmrandom['Warrior Policy'], 2)+pmr['Warrior Policy']+"      & "+round_with_padding(dssmart['Warrior Policy'], 2)+pss['Warrior Policy']+" &   "+round_with_padding(dmsmart['Warrior Policy'], 2)+pms['Warrior Policy']+" & "+round_with_padding(dsnop['Warrior Policy'], 2)+psn['Warrior Policy']+" & "+round_with_padding(dmnop['Warrior Policy'], 2)+pmn['Warrior Policy']+"         \\\\\n")
        file.write("\\textit{AttackPower}     & "+round_with_padding(dsrandom['Warrior Attack Power'], 2)+psr['Warrior Attack Power']+"                    & "+round_with_padding(dmrandom['Warrior Attack Power'], 2)+pmr['Warrior Attack Power']+"      & "+round_with_padding(dssmart['Warrior Attack Power'], 2)+pss['Warrior Attack Power']+" &   "+round_with_padding(dmsmart['Warrior Attack Power'], 2)+pms['Warrior Attack Power']+" & "+round_with_padding(dsnop['Warrior Attack Power'], 2)+psn['Warrior Attack Power']+" & "+round_with_padding(dmnop['Warrior Attack Power'], 2)+pmn['Warrior Attack Power']+"         \\\\\n")
        file.write("\\textit{HealingPower}    & "+round_with_padding(dsrandom['Warrior Healing Power'], 2)+psr['Warrior Healing Power']+"                   & "+round_with_padding(dmrandom['Warrior Healing Power'], 2)+pmr['Warrior Healing Power']+"     & "+round_with_padding(dssmart['Warrior Healing Power'], 2)+pss['Warrior Healing Power']+"  & "+round_with_padding(dmsmart['Warrior Healing Power'], 2)+pms['Warrior Healing Power']+" & "+round_with_padding(dsnop['Warrior Healing Power'], 2)+psn['Warrior Healing Power']+" & "+round_with_padding(dmnop['Warrior Healing Power'], 2)+pmn['Warrior Healing Power']+"        \\\\\n")
        file.write("\\textit{ControlChance}   & "+round_with_padding(dsrandom['Warrior Control Chance'], 2)+psr['Warrior Control Chance']+"                   & "+round_with_padding(dmrandom['Warrior Control Chance'], 2)+pmr['Warrior Control Chance']+"    & "+round_with_padding(dssmart['Warrior Control Chance'], 2)+pss['Warrior Control Chance']+"    & "+round_with_padding(dmsmart['Warrior Control Chance'], 2)+pms['Warrior Control Chance']+" & "+round_with_padding(dsnop['Warrior Control Chance'], 2)+psn['Warrior Control Chance']+"   & "+round_with_padding(dmnop['Warrior Control Chance'], 2)+pmn['Warrior Control Chance']+"        \\\\\n")
        file.write("&                           & & & & &                          \\\\\n")
        file.write("\\textbf{Agent: Mage }        &                           &                           \\\\\n")
        file.write("\\textit{MaxHealthPoints} & "+round_with_padding(dsrandom['Mage Max HP'], 2)+psr['Mage Max HP']+"                   & "+round_with_padding(dmrandom['Mage Max HP'], 2)+pmr['Mage Max HP']+" & "+round_with_padding(dssmart['Mage Max HP'], 2)+pss['Mage Max HP']+" &  "+round_with_padding(dmsmart['Mage Max HP'], 2)+pms['Mage Max HP']+" & "+round_with_padding(dsnop['Mage Max HP'], 2)+psn['Mage Max HP']+"  & "+round_with_padding(dmnop['Mage Max HP'], 2)+pmn['Mage Max HP']+"                \\\\\n")
        file.write("\\textit{Policy}     & "+round_with_padding(dsrandom['Mage Policy'], 2)+psr['Mage Policy']+"                    & "+round_with_padding(dmrandom['Mage Policy'], 2)+pmr['Mage Policy']+"      & "+round_with_padding(dssmart['Mage Policy'], 2)+pss['Mage Policy']+" &   "+round_with_padding(dmsmart['Mage Policy'], 2)+pms['Mage Policy']+" & "+round_with_padding(dsnop['Mage Policy'], 2)+psn['Mage Policy']+" & "+round_with_padding(dmnop['Mage Policy'], 2)+pmn['Mage Policy']+"         \\\\\n")
        file.write("\\textit{AttackPower}     & "+round_with_padding(dsrandom['Mage Attack Power'], 2)+psr['Mage Attack Power']+"                    & "+round_with_padding(dmrandom['Mage Attack Power'], 2)+pmr['Mage Attack Power']+"      & "+round_with_padding(dssmart['Mage Attack Power'], 2)+pss['Mage Attack Power']+" &   "+round_with_padding(dmsmart['Mage Attack Power'], 2)+pms['Mage Attack Power']+" & "+round_with_padding(dsnop['Mage Attack Power'], 2)+psn['Mage Attack Power']+" & "+round_with_padding(dmnop['Mage Attack Power'], 2)+pmn['Mage Attack Power']+"         \\\\\n")
        file.write("\\textit{HealingPower}    & "+round_with_padding(dsrandom['Mage Healing Power'], 2)+psr['Mage Healing Power']+"                   & "+round_with_padding(dmrandom['Mage Healing Power'], 2)+pmr['Mage Healing Power']+"     & "+round_with_padding(dssmart['Mage Healing Power'], 2)+pss['Mage Healing Power']+"  & "+round_with_padding(dmsmart['Mage Healing Power'], 2)+pms['Mage Healing Power']+" & "+round_with_padding(dsnop['Mage Healing Power'], 2)+psn['Mage Healing Power']+" & "+round_with_padding(dmnop['Mage Healing Power'], 2)+pmn['Mage Healing Power']+"        \\\\\n")
        file.write("\\textit{ControlChance}   & "+round_with_padding(dsrandom['Mage Control Chance'], 2)+psr['Mage Control Chance']+"                   & "+round_with_padding(dmrandom['Mage Control Chance'], 2)+pmr['Mage Control Chance']+"    & "+round_with_padding(dssmart['Mage Control Chance'], 2)+pss['Mage Control Chance']+"    & "+round_with_padding(dmsmart['Mage Control Chance'], 2)+pms['Mage Control Chance']+" & "+round_with_padding(dsnop['Mage Control Chance'], 2)+psn['Mage Control Chance']+"   & "+round_with_padding(dmnop['Mage Control Chance'], 2)+pmn['Mage Control Chance']+"        \\\\\n")
        file.write("&                           & & & & &                          \\\\\n")
        file.write("\\textbf{Agent: Priest }        &                           &                           \\\\\n")
        file.write("\\textit{MaxHealthPoints} & "+round_with_padding(dsrandom['Priest Max HP'], 2)+psr['Priest Max HP']+"                   & "+round_with_padding(dmrandom['Priest Max HP'], 2)+pmr['Priest Max HP']+" & "+round_with_padding(dssmart['Priest Max HP'], 2)+pss['Priest Max HP']+" &  "+round_with_padding(dmsmart['Priest Max HP'], 2)+pms['Priest Max HP']+" & "+round_with_padding(dsnop['Priest Max HP'], 2)+psn['Priest Max HP']+"  & "+round_with_padding(dmnop['Priest Max HP'], 2)+pmn['Priest Max HP']+"                \\\\\n")
        file.write("\\textit{Policy}     & "+round_with_padding(dsrandom['Priest Policy'], 2)+psr['Priest Policy']+"                    & "+round_with_padding(dmrandom['Priest Policy'], 2)+pmr['Priest Policy']+"      & "+round_with_padding(dssmart['Priest Policy'], 2)+pss['Priest Policy']+" &   "+round_with_padding(dmsmart['Priest Policy'], 2)+pms['Priest Policy']+" & "+round_with_padding(dsnop['Priest Policy'], 2)+psn['Priest Policy']+" & "+round_with_padding(dmnop['Priest Policy'], 2)+pmn['Priest Policy']+"         \\\\\n")
        file.write("\\textit{AttackPower}     & "+round_with_padding(dsrandom['Priest Attack Power'], 2)+psr['Priest Attack Power']+"                    & "+round_with_padding(dmrandom['Priest Attack Power'], 2)+pmr['Priest Attack Power']+"      & "+round_with_padding(dssmart['Priest Attack Power'], 2)+pss['Priest Attack Power']+" &   "+round_with_padding(dmsmart['Priest Attack Power'], 2)+pms['Priest Attack Power']+" & "+round_with_padding(dsnop['Priest Attack Power'], 2)+psn['Priest Attack Power']+" & "+round_with_padding(dmnop['Priest Attack Power'], 2)+pmn['Priest Attack Power']+"         \\\\\n")
        file.write("\\textit{HealingPower}    & "+round_with_padding(dsrandom['Priest Healing Power'], 2)+psr['Priest Healing Power']+"                   & "+round_with_padding(dmrandom['Priest Healing Power'], 2)+pmr['Priest Healing Power']+"     & "+round_with_padding(dssmart['Priest Healing Power'], 2)+pss['Priest Healing Power']+"  & "+round_with_padding(dmsmart['Priest Healing Power'], 2)+pms['Priest Healing Power']+" & "+round_with_padding(dsnop['Priest Healing Power'], 2)+psn['Priest Healing Power']+" & "+round_with_padding(dmnop['Priest Healing Power'], 2)+pmn['Priest Healing Power']+"        \\\\\n")
        file.write("\\textit{ControlChance}   & "+round_with_padding(dsrandom['Priest Control Chance'], 2)+psr['Priest Control Chance']+"                   & "+round_with_padding(dmrandom['Priest Control Chance'], 2)+pmr['Priest Control Chance']+"    & "+round_with_padding(dssmart['Priest Control Chance'], 2)+pss['Priest Control Chance']+"    & "+round_with_padding(dmsmart['Priest Control Chance'], 2)+pms['Priest Control Chance']+" & "+round_with_padding(dsnop['Priest Control Chance'], 2)+psn['Priest Control Chance']+"   & "+round_with_padding(dmnop['Priest Control Chance'], 2)+pmn['Priest Control Chance']+"        \\\\\n")
        file.write("\end{tabular}\n")
        file.write("\end{table}\n")