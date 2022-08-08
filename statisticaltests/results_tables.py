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

def normalize(voc, constant):
    for entry in voc:
        voc[entry] /= constant
    return voc

def open_close(dict, index, feat):
    print(dict[0])
    if dict[index][feat] == "*":
        return "\\textit{", "}"
    elif dict[index][feat] == "**":
        return "\\uline{", "}"
    elif dict[index][feat] == "***":
        return "\\textbf{", "}"
    else:
        return "", ""

if __name__ == '__main__':
    with open("results.tex", "w") as file:
        minim = 9999999
        maxim = 0
        file.write("\\begin{tabular}{lllllllll}\n")
        for pol_a in ['random', 'smart', 'nothing', 'rl']:
            sbrandom = open("exact_shapley_a" + pol_a + "_brandom_results.json")
            mbrandom = open("exact_myerson_a" + pol_a + "_brandom_results.json")
            sbsmart = open("exact_shapley_a" + pol_a + "_bsmart_results.json")
            mbsmart = open("exact_myerson_a" + pol_a + "_bsmart_results.json")
            sbnop = open("exact_shapley_a" + pol_a + "_bnothing_results.json")
            mbnop = open("exact_myerson_a" + pol_a + "_bnothing_results.json")
            sbrl = open("exact_shapley_a" + pol_a + "_brl_results.json")
            mbrl = open("exact_myerson_a" + pol_a + "_brl_results.json")

            dsrandom = json.load(sbrandom)
            dmrandom = json.load(mbrandom)
            dssmart = json.load(sbsmart)
            dmsmart = json.load(mbsmart)
            dsnop = json.load(sbnop)
            dmnop = json.load(mbnop)
            dsrl = json.load(sbrl)
            dmrl = json.load(mbrl)

            sbrandom.close()
            mbrandom.close()
            sbsmart.close()
            mbsmart.close()
            sbnop.close()
            mbnop.close()
            sbrl.close()
            mbrl.close()

            data = np.load('exact_myerson_a' + pol_a + '_bnothing.npz')
            vmn = data['v']
            score_mn = np.sum(np.mean(vmn, axis=1))
            data = np.load('exact_myerson_a' + pol_a + '_brandom.npz')
            vmr = data['v']
            score_mr = np.sum(np.mean(vmr, axis=1))
            data = np.load('exact_myerson_a' + pol_a + '_bsmart.npz')
            vms = data['v']
            score_ms = np.sum(np.mean(vms, axis=1))
            data = np.load('exact_myerson_a' + pol_a + '_brl.npz')
            vml = data['v']
            score_ml = np.sum(np.mean(vml, axis=1))

            data = np.load('exact_shapley_a' + pol_a + '_bnothing.npz')
            vsn = data['v']
            score_sn = np.sum(np.mean(vsn, axis=1))

            data = np.load('exact_shapley_a' + pol_a + '_brandom.npz')
            vsr = data['v']
            score_sr = np.sum(np.mean(vsr, axis=1))

            data = np.load('exact_shapley_a' + pol_a + '_bsmart.npz')
            vss = data['v']
            score_ss = np.sum(np.mean(vss, axis=1))

            data = np.load('exact_shapley_a' + pol_a + '_brl.npz')
            vsl = data['v']
            score_sl = np.sum(np.mean(vsl, axis=1))

            attributes = list(dsrandom.keys())
            zeroes = np.zeros(vsn.shape[1])
            psr = {}
            pmr = {}
            psn = {}
            pmn = {}
            pss = {}
            pms = {}
            psl = {}
            pml = {}

            attr = ['Warrior HP', 'Warrior Policy', 'Warrior AP', 'Warrior HealingP', 'Warrior CC',
                    'Mage HP', 'Mage Policy', 'Mage AP', 'Mage HealingP', 'Mage CC',
                    'Priest HP', 'Priest Policy', 'Priest AP', 'Priest HealingP', 'Priest CC']

            diff_shap_mye_random = {}
            diff_shap_mye_smart = {}
            diff_shap_mye_smart = {}
            diff_shap_mye_rl = {}

            datas = [[vsr, vmr], [vss, vms], [vsn, vmn], [vsl, vml]]
            dicts = [diff_shap_mye_random, diff_shap_mye_smart, diff_shap_mye_smart, diff_shap_mye_rl]

            for d in range(len(datas)):
                for i in range(vsr.shape[0]):
                    s, p = stats.mannwhitneyu(x=datas[d][0][i], y=datas[d][1][i])
                    # s, p = stats.mannwhitneyu(x=shapley[i], y=zeroes)
                    if p < 0.001:
                        #print(attr[i])
                        #print(s, p)
                        #print("STATISTICALLY DIFFERENT ***")
                        dicts[d][str(attr[i])] = "***"
                    elif p < 0.01:
                        #print(attr[i])
                        #print(s, p)
                        #print("STATISTICALLY DIFFERENT **")
                        dicts[d][str(attr[i])] = "**"
                    elif p < 0.05:
                        #print(attr[i])
                        #print(s, p)
                        #print("STATISTICALLY DIFFERENT *")
                        dicts[d][str(attr[i])] = "*"
                    else:
                        dicts[d][str(attr[i])] = ""
                        pass
                    print("")

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

                if np.all(vsn[i] != 0):
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

                if np.all(vsl[i] != 0):
                    res, pv = stats.mannwhitneyu(vsl[i], zeroes)
                    if pv < 0.001:
                        psl[attributes[i]] = "${}^{***}$"
                    elif pv < 0.01:
                        psl[attributes[i]] = "${}^{**}$"
                    elif pv < 0.05:
                        psl[attributes[i]] = "${}^{*}$"
                    else:
                        psl[attributes[i]] = ""
                else:
                    psl[attributes[i]] = ""

                if np.all(vml[i] != 0):
                    res, pv = stats.mannwhitneyu(vml[i], zeroes)
                    if pv < 0.001:
                        pml[attributes[i]] = "${}^{***}$"
                    elif pv < 0.01:
                        pml[attributes[i]] = "${}^{**}$"
                    elif pv < 0.05:
                        pml[attributes[i]] = "${}^{*}$"
                    else:
                        pml[attributes[i]] = ""
                else:
                    pml[attributes[i]] = ""

            if 'Time' not in dsrandom.keys():
                dsrandom['Time'] = 0
            if 'Time' not in dmrandom.keys():
                dmrandom['Time'] = 0

            if 'Time' not in dssmart.keys():
                dssmart['Time'] = 0
            if 'Time' not in dmsmart.keys():
                dmsmart['Time'] = 0

            if 'Time' not in dsnop.keys():
                dsnop['Time'] = 0
            if 'Time' not in dmnop.keys():
                dmnop['Time'] = 0

            if 'Time' not in dsrl.keys():
                dsrl['Time'] = 0
            if 'Time' not in dmrl.keys():
                dmrl['Time'] = 0

            tempmin = min([dsrandom['Time']/dmrandom['Time'], dssmart['Time']/dmsmart['Time'], dsnop['Time']/dmnop['Time'], dsrl['Time']/dmrl['Time']])
            tempmax = max([dsrandom['Time']/dmrandom['Time'], dssmart['Time']/dmsmart['Time'], dsnop['Time']/dmnop['Time'], dsrl['Time']/dmrl['Time']])

            if tempmin < minim:
                minim = tempmin

            if tempmax > maxim:
                maxim = tempmax

            file.write("&\multicolumn{2}{c}{"+pol_a.title()+" vs Random}&\multicolumn{2}{c}{"+pol_a.title()+" vs Smart}&\multicolumn{2}{c}{"+pol_a.title()+" vs No-Op}&\multicolumn{2}{c}{"+pol_a.title()+" vs A2C}\\\\\n")
            file.write("\\textbf{Feature}         & \\textit{\\textbf{Shapley}} & \\textit{\\textbf{Myerson}}& \\textit{\\textbf{Shapley}} & \\textit{\\textbf{Myerson}}& \\textit{\\textbf{Shapley}} & \\textit{\\textbf{Myerson}}& \\textit{\\textbf{Shapley}} & \\textit{\\textbf{Myerson}} \\\\\n")
            file.write("\\textbf{Total Score $\Sigma$} & "+round_with_padding(score_sr, 2)+"&"+round_with_padding(score_mr, 2)+"&"+round_with_padding(score_ss, 2)+"&"+round_with_padding(score_ms, 2)+"&"+round_with_padding(score_sn, 2)+"&"+round_with_padding(score_mn, 2)+"&"+round_with_padding(score_sl, 2)+"&"+round_with_padding(score_ml, 2)+" \\\\\\n")
            file.write("\\textbf{Comp. Time (s)} & "+round_with_padding(dsrandom['Time'], 2)+"&"+round_with_padding(dmrandom['Time'], 2)+"&"+round_with_padding(dssmart['Time'], 2)+"&"+round_with_padding(dmsmart['Time'], 2)+"&"+round_with_padding(dsnop['Time'], 2)+"&"+round_with_padding(dmnop['Time'], 2)+"&"+round_with_padding(dsrl['Time'], 2)+"&"+round_with_padding(dmrl['Time'], 2)+" \\\\\\n")

            file.write("\hline\n")
            file.write("&                           & & & & &                          & &\\\\\n")
            file.write("\\textbf{Agent: Warrior }        &                           &                           & &\\\\\n")
            file.write("\\textit{MaxHealthPoints} & "+open_close(dicts,0,"Warrior HP")[0]+round_with_padding(dsrandom['Warrior Max HP'], 2)+psr['Warrior Max HP']+open_close(dicts,0,"Warrior HP")[1]+"                   & "+open_close(dicts,0,"Warrior HP")[0]+round_with_padding(dmrandom['Warrior Max HP'], 2)+pmr['Warrior Max HP']+open_close(dicts,0,"Warrior HP")[1]+" & "+open_close(dicts,1,"Warrior HP")[0]+round_with_padding(dssmart['Warrior Max HP'], 2)+pss['Warrior Max HP']+open_close(dicts,1,"Warrior HP")[1]+" &  "+open_close(dicts,1,"Warrior HP")[0]+round_with_padding(dmsmart['Warrior Max HP'], 2)+pms['Warrior Max HP']+open_close(dicts,1,"Warrior HP")[1]+" & "+open_close(dicts,2,"Warrior HP")[0]+round_with_padding(dsnop['Warrior Max HP'], 2)+psn['Warrior Max HP']+open_close(dicts,2,"Warrior HP")[1]+"  & "+open_close(dicts,2,"Warrior HP")[0]+round_with_padding(dmnop['Warrior Max HP'], 2)+pmn['Warrior Max HP']+open_close(dicts,2,"Warrior HP")[1]+" & "+open_close(dicts,3,"Warrior HP")[0]+round_with_padding(dsrl['Warrior Max HP'], 2)+psl['Warrior Max HP']+open_close(dicts,3,"Warrior HP")[1]+"  & "+open_close(dicts,3,"Warrior HP")[0]+round_with_padding(dmrl['Warrior Max HP'], 2)+pml['Warrior Max HP']+open_close(dicts,3,"Warrior HP")[1]+"                \\\\\n")
            file.write("\\textit{Policy}     & "+open_close(dicts,0,"Warrior Policy")[0]+round_with_padding(dsrandom['Warrior Policy'], 2)+psr['Warrior Policy']+open_close(dicts,0,"Warrior Policy")[1]+"                    & "+open_close(dicts,0,"Warrior Policy")[0]+round_with_padding(dmrandom['Warrior Policy'], 2)+pmr['Warrior Policy']+open_close(dicts,0,"Warrior Policy")[1]+"      & "+open_close(dicts,1,"Warrior Policy")[0]+round_with_padding(dssmart['Warrior Policy'], 2)+pss['Warrior Policy']+open_close(dicts,1,"Warrior Policy")[1]+" &   "+open_close(dicts,1,"Warrior Policy")[0]+round_with_padding(dmsmart['Warrior Policy'], 2)+pms['Warrior Policy']+open_close(dicts,1,"Warrior Policy")[1]+" & "+open_close(dicts,2,"Warrior Policy")[0]+round_with_padding(dsnop['Warrior Policy'], 2)+psn['Warrior Policy']+open_close(dicts,2,"Warrior Policy")[1]+" & "+open_close(dicts,2,"Warrior Policy")[0]+round_with_padding(dmnop['Warrior Policy'], 2)+pmn['Warrior Policy']+open_close(dicts,2,"Warrior Policy")[1]+" & "+open_close(dicts,3,"Warrior Policy")[0]+round_with_padding(dsrl['Warrior Policy'], 2)+psl['Warrior Policy']+open_close(dicts,3,"Warrior Policy")[1]+"  & "+open_close(dicts,3,"Warrior Policy")[0]+round_with_padding(dmrl['Warrior Policy'], 2)+pml['Warrior Policy']+open_close(dicts,3,"Warrior Policy")[1]+"         \\\\\n")
            file.write("\\textit{AttackPower}     & "+open_close(dicts,0,"Warrior AP")[0]+round_with_padding(dsrandom['Warrior Attack Power'], 2)+psr['Warrior Attack Power']+open_close(dicts,0,"Warrior AP")[1]+"                    & "+open_close(dicts,0,"Warrior AP")[0]+round_with_padding(dmrandom['Warrior Attack Power'], 2)+pmr['Warrior Attack Power']+open_close(dicts,0,"Warrior AP")[1]+"      & "+open_close(dicts,1,"Warrior AP")[0]+round_with_padding(dssmart['Warrior Attack Power'], 2)+pss['Warrior Attack Power']+open_close(dicts,1,"Warrior AP")[1]+" &   "+open_close(dicts,1,"Warrior AP")[0]+round_with_padding(dmsmart['Warrior Attack Power'], 2)+pms['Warrior Attack Power']+open_close(dicts,1,"Warrior AP")[1]+" & "+open_close(dicts,2,"Warrior AP")[0]+round_with_padding(dsnop['Warrior Attack Power'], 2)+psn['Warrior Attack Power']+open_close(dicts,2,"Warrior AP")[1]+" & "+open_close(dicts,2,"Warrior AP")[0]+round_with_padding(dmnop['Warrior Attack Power'], 2)+pmn['Warrior Attack Power']+open_close(dicts,2,"Warrior AP")[1]+" & "+open_close(dicts,3,"Warrior AP")[0]+round_with_padding(dsrl['Warrior Attack Power'], 2)+psl['Warrior Attack Power']+open_close(dicts,3,"Warrior AP")[1]+"  & "+open_close(dicts,3,"Warrior AP")[0]+round_with_padding(dmrl['Warrior Attack Power'], 2)+pml['Warrior Attack Power']+open_close(dicts,3,"Warrior AP")[1]+"         \\\\\n")
            file.write("\\textit{HealingPower}    & "+open_close(dicts,0,"Warrior HealingP")[0]+round_with_padding(dsrandom['Warrior Healing Power'], 2)+psr['Warrior Healing Power']+open_close(dicts,0,"Warrior HealingP")[1]+"                   & "+open_close(dicts,0,"Warrior HealingP")[0]+round_with_padding(dmrandom['Warrior Healing Power'], 2)+pmr['Warrior Healing Power']+open_close(dicts,0,"Warrior HealingP")[1]+"     & "+open_close(dicts,1,"Warrior HealingP")[0]+round_with_padding(dssmart['Warrior Healing Power'], 2)+pss['Warrior Healing Power']+open_close(dicts,1,"Warrior HealingP")[1]+"  & "+open_close(dicts,1,"Warrior HealingP")[0]+round_with_padding(dmsmart['Warrior Healing Power'], 2)+pms['Warrior Healing Power']+open_close(dicts,1,"Warrior HealingP")[1]+" & "+open_close(dicts,2,"Warrior HealingP")[0]+round_with_padding(dsnop['Warrior Healing Power'], 2)+psn['Warrior Healing Power']+open_close(dicts,2,"Warrior HealingP")[1]+" & "+open_close(dicts,2,"Warrior HealingP")[0]+round_with_padding(dmnop['Warrior Healing Power'], 2)+pmn['Warrior Healing Power']+open_close(dicts,2,"Warrior HealingP")[1]+" & "+open_close(dicts,3,"Warrior HealingP")[0]+round_with_padding(dsrl['Warrior Healing Power'], 2)+psl['Warrior Healing Power']+open_close(dicts,3,"Warrior HealingP")[1]+"  & "+open_close(dicts,3,"Warrior HealingP")[0]+round_with_padding(dmrl['Warrior Healing Power'], 2)+pml['Warrior Healing Power']+open_close(dicts,3,"Warrior HealingP")[1]+"        \\\\\n")
            file.write("\\textit{ControlChance}   & "+open_close(dicts,0,"Warrior CC")[0]+round_with_padding(dsrandom['Warrior Control Chance'], 2)+psr['Warrior Control Chance']+open_close(dicts,0,"Warrior CC")[1]+"                   & "+open_close(dicts,0,"Warrior CC")[0]+round_with_padding(dmrandom['Warrior Control Chance'], 2)+pmr['Warrior Control Chance']+open_close(dicts,0,"Warrior CC")[1]+"    & "+open_close(dicts,1,"Warrior CC")[0]+round_with_padding(dssmart['Warrior Control Chance'], 2)+pss['Warrior Control Chance']+open_close(dicts,1,"Warrior CC")[1]+"    & "+open_close(dicts,1,"Warrior CC")[0]+round_with_padding(dmsmart['Warrior Control Chance'], 2)+pms['Warrior Control Chance']+open_close(dicts,1,"Warrior CC")[1]+" & "+open_close(dicts,2,"Warrior CC")[0]+round_with_padding(dsnop['Warrior Control Chance'], 2)+psn['Warrior Control Chance']+open_close(dicts,2,"Warrior CC")[1]+"   & "+open_close(dicts,2,"Warrior CC")[0]+round_with_padding(dmnop['Warrior Control Chance'], 2)+pmn['Warrior Control Chance']+open_close(dicts,2,"Warrior CC")[1]+" & "+open_close(dicts,3,"Warrior CC")[0]+round_with_padding(dsrl['Warrior Control Chance'], 2)+psl['Warrior Control Chance']+open_close(dicts,3,"Warrior CC")[1]+"  & "+open_close(dicts,3,"Warrior CC")[0]+round_with_padding(dmrl['Warrior Control Chance'], 2)+pml['Warrior Control Chance']+open_close(dicts,3,"Warrior CC")[1]+"        \\\\\n")
            file.write("&                           & & & & &                          & &\\\\\n")
            file.write("\\textbf{Agent: Mage }        &                           &                           & &\\\\\n")
            file.write("\\textit{MaxHealthPoints} & "+open_close(dicts,0,"Mage HP")[0]+round_with_padding(dsrandom['Mage Max HP'], 2)+psr['Mage Max HP']+open_close(dicts,0,"Mage HP")[1]+"                   & "+open_close(dicts,0,"Mage HP")[0]+round_with_padding(dmrandom['Mage Max HP'], 2)+pmr['Mage Max HP']+open_close(dicts,0,"Mage HP")[1]+" & "+open_close(dicts,1,"Mage HP")[0]+round_with_padding(dssmart['Mage Max HP'], 2)+pss['Mage Max HP']+open_close(dicts,1,"Mage HP")[1]+" &  "+open_close(dicts,1,"Mage HP")[0]+round_with_padding(dmsmart['Mage Max HP'], 2)+pms['Mage Max HP']+open_close(dicts,1,"Mage HP")[1]+" & "+open_close(dicts,2,"Mage HP")[0]+round_with_padding(dsnop['Mage Max HP'], 2)+psn['Mage Max HP']+open_close(dicts,2,"Mage HP")[1]+"  & "+open_close(dicts,2,"Mage HP")[0]+round_with_padding(dmnop['Mage Max HP'], 2)+pmn['Mage Max HP']+open_close(dicts,2,"Mage HP")[1]+" & "+open_close(dicts,3,"Mage HP")[0]+round_with_padding(dsrl['Mage Max HP'], 2)+psl['Mage Max HP']+open_close(dicts,3,"Mage HP")[1]+"  & "+open_close(dicts,3,"Mage HP")[0]+round_with_padding(dmrl['Mage Max HP'], 2)+pml['Mage Max HP']+open_close(dicts,3,"Mage HP")[1]+"                \\\\\n")
            file.write("\\textit{Policy}     & "+open_close(dicts,0,"Mage Policy")[0]+round_with_padding(dsrandom['Mage Policy'], 2)+psr['Mage Policy']+open_close(dicts,0,"Mage Policy")[1]+"                    & "+open_close(dicts,0,"Mage Policy")[0]+round_with_padding(dmrandom['Mage Policy'], 2)+pmr['Mage Policy']+open_close(dicts,0,"Mage Policy")[1]+"      & "+open_close(dicts,1,"Mage Policy")[0]+round_with_padding(dssmart['Mage Policy'], 2)+pss['Mage Policy']+open_close(dicts,1,"Mage Policy")[1]+" &   "+open_close(dicts,1,"Mage Policy")[0]+round_with_padding(dmsmart['Mage Policy'], 2)+pms['Mage Policy']+open_close(dicts,1,"Mage Policy")[1]+" & "+open_close(dicts,2,"Mage Policy")[0]+round_with_padding(dsnop['Mage Policy'], 2)+psn['Mage Policy']+open_close(dicts,2,"Mage Policy")[1]+" & "+open_close(dicts,2,"Mage Policy")[0]+round_with_padding(dmnop['Mage Policy'], 2)+pmn['Mage Policy']+open_close(dicts,2,"Mage Policy")[1]+" & "+open_close(dicts,3,"Mage Policy")[0]+round_with_padding(dsrl['Mage Policy'], 2)+psl['Mage Policy']+open_close(dicts,3,"Mage Policy")[1]+"  & "+open_close(dicts,3,"Mage Policy")[0]+round_with_padding(dmrl['Mage Policy'], 2)+pml['Mage Policy']+open_close(dicts,3,"Mage Policy")[1]+"         \\\\\n")
            file.write("\\textit{AttackPower}     & "+open_close(dicts,0,"Mage AP")[0]+round_with_padding(dsrandom['Mage Attack Power'], 2)+psr['Mage Attack Power']+open_close(dicts,0,"Mage AP")[1]+"                    & "+open_close(dicts,0,"Mage AP")[0]+round_with_padding(dmrandom['Mage Attack Power'], 2)+pmr['Mage Attack Power']+open_close(dicts,0,"Mage AP")[1]+"      & "+open_close(dicts,1,"Mage AP")[0]+round_with_padding(dssmart['Mage Attack Power'], 2)+pss['Mage Attack Power']+open_close(dicts,1,"Mage AP")[1]+" &   "+open_close(dicts,1,"Mage AP")[0]+round_with_padding(dmsmart['Mage Attack Power'], 2)+pms['Mage Attack Power']+open_close(dicts,1,"Mage AP")[1]+" & "+open_close(dicts,2,"Mage AP")[0]+round_with_padding(dsnop['Mage Attack Power'], 2)+psn['Mage Attack Power']+open_close(dicts,2,"Mage AP")[1]+" & "+open_close(dicts,2,"Mage AP")[0]+round_with_padding(dmnop['Mage Attack Power'], 2)+pmn['Mage Attack Power']+open_close(dicts,2,"Mage AP")[1]+" & "+open_close(dicts,3,"Mage AP")[0]+round_with_padding(dsrl['Mage Attack Power'], 2)+psl['Mage Attack Power']+open_close(dicts,3,"Mage AP")[1]+"  & "+open_close(dicts,3,"Mage AP")[0]+round_with_padding(dmrl['Mage Attack Power'], 2)+pml['Mage Attack Power']+open_close(dicts,3,"Mage AP")[1]+"         \\\\\n")
            file.write("\\textit{HealingPower}    & "+open_close(dicts,0,"Mage HealingP")[0]+round_with_padding(dsrandom['Mage Healing Power'], 2)+psr['Mage Healing Power']+open_close(dicts,0,"Mage HealingP")[1]+"                   & "+open_close(dicts,0,"Mage HealingP")[0]+round_with_padding(dmrandom['Mage Healing Power'], 2)+pmr['Mage Healing Power']+open_close(dicts,0,"Mage HealingP")[1]+"     & "+open_close(dicts,1,"Mage HealingP")[0]+round_with_padding(dssmart['Mage Healing Power'], 2)+pss['Mage Healing Power']+open_close(dicts,1,"Mage HealingP")[1]+"  & "+open_close(dicts,1,"Mage HealingP")[0]+round_with_padding(dmsmart['Mage Healing Power'], 2)+pms['Mage Healing Power']+open_close(dicts,1,"Mage HealingP")[1]+" & "+open_close(dicts,2,"Mage HealingP")[0]+round_with_padding(dsnop['Mage Healing Power'], 2)+psn['Mage Healing Power']+open_close(dicts,2,"Mage HealingP")[1]+" & "+open_close(dicts,2,"Mage HealingP")[0]+round_with_padding(dmnop['Mage Healing Power'], 2)+pmn['Mage Healing Power']+open_close(dicts,2,"Mage HealingP")[1]+" & "+open_close(dicts,3,"Mage HealingP")[0]+round_with_padding(dsrl['Mage Healing Power'], 2)+psl['Mage Healing Power']+open_close(dicts,3,"Mage HealingP")[1]+"  & "+open_close(dicts,3,"Mage HealingP")[0]+round_with_padding(dmrl['Mage Healing Power'], 2)+pml['Mage Healing Power']+open_close(dicts,3,"Mage HealingP")[1]+"        \\\\\n")
            file.write("\\textit{ControlChance}   & "+open_close(dicts,0,"Mage CC")[0]+round_with_padding(dsrandom['Mage Control Chance'], 2)+psr['Mage Control Chance']+open_close(dicts,0,"Mage CC")[1]+"                   & "+open_close(dicts,0,"Mage CC")[0]+round_with_padding(dmrandom['Mage Control Chance'], 2)+pmr['Mage Control Chance']+open_close(dicts,0,"Mage CC")[1]+"    & "+open_close(dicts,1,"Mage CC")[0]+round_with_padding(dssmart['Mage Control Chance'], 2)+pss['Mage Control Chance']+open_close(dicts,1,"Mage CC")[1]+"    & "+open_close(dicts,1,"Mage CC")[0]+round_with_padding(dmsmart['Mage Control Chance'], 2)+pms['Mage Control Chance']+open_close(dicts,1,"Mage CC")[1]+" & "+open_close(dicts,2,"Mage CC")[0]+round_with_padding(dsnop['Mage Control Chance'], 2)+psn['Mage Control Chance']+open_close(dicts,2,"Mage CC")[1]+"   & "+open_close(dicts,2,"Mage CC")[0]+round_with_padding(dmnop['Mage Control Chance'], 2)+pmn['Mage Control Chance']+open_close(dicts,2,"Mage CC")[1]+" & "+open_close(dicts,3,"Mage CC")[0]+round_with_padding(dsrl['Mage Control Chance'], 2)+psl['Mage Control Chance']+open_close(dicts,3,"Mage CC")[1]+"  & "+open_close(dicts,3,"Mage CC")[0]+round_with_padding(dmrl['Mage Control Chance'], 2)+pml['Mage Control Chance']+open_close(dicts,3,"Mage CC")[1]+"        \\\\\n")
            file.write("&                           & & & & &                          & &\\\\\n")
            file.write("\\textbf{Agent: Priest }        &                           &                           & &\\\\\n")
            file.write("\\textit{MaxHealthPoints} & "+open_close(dicts,0,"Priest HP")[0]+round_with_padding(dsrandom['Priest Max HP'], 2)+psr['Priest Max HP']+open_close(dicts,0,"Priest HP")[1]+"                   & "+open_close(dicts,0,"Priest HP")[0]+round_with_padding(dmrandom['Priest Max HP'], 2)+pmr['Priest Max HP']+open_close(dicts,0,"Priest HP")[1]+" & "+open_close(dicts,1,"Priest HP")[0]+round_with_padding(dssmart['Priest Max HP'], 2)+pss['Priest Max HP']+open_close(dicts,1,"Priest HP")[1]+" &  "+open_close(dicts,1,"Priest HP")[0]+round_with_padding(dmsmart['Priest Max HP'], 2)+pms['Priest Max HP']+open_close(dicts,1,"Priest HP")[1]+" & "+open_close(dicts,2,"Priest HP")[0]+round_with_padding(dsnop['Priest Max HP'], 2)+psn['Priest Max HP']+open_close(dicts,2,"Priest HP")[1]+"  & "+open_close(dicts,2,"Priest HP")[0]+round_with_padding(dmnop['Priest Max HP'], 2)+pmn['Priest Max HP']+open_close(dicts,2,"Priest HP")[1]+" & "+open_close(dicts,3,"Priest HP")[0]+round_with_padding(dsrl['Priest Max HP'], 2)+psl['Priest Max HP']+open_close(dicts,3,"Priest HP")[1]+"  & "+open_close(dicts,3,"Priest HP")[0]+round_with_padding(dmrl['Priest Max HP'], 2)+pml['Priest Max HP']+open_close(dicts,3,"Priest HP")[1]+"                \\\\\n")
            file.write("\\textit{Policy}     & "+open_close(dicts,0,"Priest Policy")[0]+round_with_padding(dsrandom['Priest Policy'], 2)+psr['Priest Policy']+open_close(dicts,0,"Priest Policy")[1]+"                    & "+open_close(dicts,0,"Priest Policy")[0]+round_with_padding(dmrandom['Priest Policy'], 2)+pmr['Priest Policy']+open_close(dicts,0,"Priest Policy")[1]+"      & "+open_close(dicts,1,"Priest Policy")[0]+round_with_padding(dssmart['Priest Policy'], 2)+pss['Priest Policy']+open_close(dicts,1,"Priest Policy")[1]+" &   "+open_close(dicts,1,"Priest Policy")[0]+round_with_padding(dmsmart['Priest Policy'], 2)+pms['Priest Policy']+open_close(dicts,1,"Priest Policy")[1]+" & "+open_close(dicts,2,"Priest Policy")[0]+round_with_padding(dsnop['Priest Policy'], 2)+psn['Priest Policy']+open_close(dicts,2,"Priest Policy")[1]+" & "+open_close(dicts,2,"Priest Policy")[0]+round_with_padding(dmnop['Priest Policy'], 2)+pmn['Priest Policy']+open_close(dicts,2,"Priest Policy")[1]+" & "+open_close(dicts,3,"Priest Policy")[0]+round_with_padding(dsrl['Priest Policy'], 2)+psl['Priest Policy']+open_close(dicts,3,"Priest Policy")[1]+"  & "+open_close(dicts,3,"Priest Policy")[0]+round_with_padding(dmrl['Priest Policy'], 2)+pml['Priest Policy']+open_close(dicts,3,"Priest Policy")[1]+"         \\\\\n")
            file.write("\\textit{AttackPower}     & "+open_close(dicts,0,"Priest AP")[0]+round_with_padding(dsrandom['Priest Attack Power'], 2)+psr['Priest Attack Power']+open_close(dicts,0,"Priest AP")[1]+"                    & "+open_close(dicts,0,"Priest AP")[0]+round_with_padding(dmrandom['Priest Attack Power'], 2)+pmr['Priest Attack Power']+open_close(dicts,0,"Priest AP")[1]+"      & "+open_close(dicts,1,"Priest AP")[0]+round_with_padding(dssmart['Priest Attack Power'], 2)+pss['Priest Attack Power']+open_close(dicts,1,"Priest AP")[1]+" &   "+open_close(dicts,1,"Priest AP")[0]+round_with_padding(dmsmart['Priest Attack Power'], 2)+pms['Priest Attack Power']+open_close(dicts,1,"Priest AP")[1]+" & "+open_close(dicts,2,"Priest AP")[0]+round_with_padding(dsnop['Priest Attack Power'], 2)+psn['Priest Attack Power']+open_close(dicts,2,"Priest AP")[1]+" & "+open_close(dicts,2,"Priest AP")[0]+round_with_padding(dmnop['Priest Attack Power'], 2)+pmn['Priest Attack Power']+open_close(dicts,2,"Priest AP")[1]+" & "+open_close(dicts,3,"Priest AP")[0]+round_with_padding(dsrl['Priest Attack Power'], 2)+psl['Priest Attack Power']+open_close(dicts,3,"Priest AP")[1]+"  & "+open_close(dicts,3,"Priest AP")[0]+round_with_padding(dmrl['Priest Attack Power'], 2)+pml['Priest Attack Power']+open_close(dicts,3,"Priest AP")[1]+"         \\\\\n")
            file.write("\\textit{HealingPower}    & "+open_close(dicts,0,"Priest HealingP")[0]+round_with_padding(dsrandom['Priest Healing Power'], 2)+psr['Priest Healing Power']+open_close(dicts,0,"Priest HealingP")[1]+"                   & "+open_close(dicts,0,"Priest HealingP")[0]+round_with_padding(dmrandom['Priest Healing Power'], 2)+pmr['Priest Healing Power']+open_close(dicts,0,"Priest HealingP")[1]+"     & "+open_close(dicts,1,"Priest HealingP")[0]+round_with_padding(dssmart['Priest Healing Power'], 2)+pss['Priest Healing Power']+open_close(dicts,1,"Priest HealingP")[1]+"  & "+open_close(dicts,1,"Priest HealingP")[0]+round_with_padding(dmsmart['Priest Healing Power'], 2)+pms['Priest Healing Power']+open_close(dicts,1,"Priest HealingP")[1]+" & "+open_close(dicts,2,"Priest HealingP")[0]+round_with_padding(dsnop['Priest Healing Power'], 2)+psn['Priest Healing Power']+open_close(dicts,2,"Priest HealingP")[1]+" & "+open_close(dicts,2,"Priest HealingP")[0]+round_with_padding(dmnop['Priest Healing Power'], 2)+pmn['Priest Healing Power']+open_close(dicts,2,"Priest HealingP")[1]+" & "+open_close(dicts,3,"Priest HealingP")[0]+round_with_padding(dsrl['Priest Healing Power'], 2)+psl['Priest Healing Power']+open_close(dicts,3,"Priest HealingP")[1]+"  & "+open_close(dicts,3,"Priest HealingP")[0]+round_with_padding(dmrl['Priest Healing Power'], 2)+pml['Priest Healing Power']+open_close(dicts,3,"Priest HealingP")[1]+"        \\\\\n")
            file.write("\\textit{ControlChance}   & "+open_close(dicts,0,"Priest CC")[0]+round_with_padding(dsrandom['Priest Control Chance'], 2)+psr['Priest Control Chance']+open_close(dicts,0,"Priest CC")[1]+"                   & "+open_close(dicts,0,"Priest CC")[0]+round_with_padding(dmrandom['Priest Control Chance'], 2)+pmr['Priest Control Chance']+open_close(dicts,0,"Priest CC")[1]+"    & "+open_close(dicts,1,"Priest CC")[0]+round_with_padding(dssmart['Priest Control Chance'], 2)+pss['Priest Control Chance']+open_close(dicts,1,"Priest CC")[1]+"    & "+open_close(dicts,1,"Priest CC")[0]+round_with_padding(dmsmart['Priest Control Chance'], 2)+pms['Priest Control Chance']+open_close(dicts,1,"Priest CC")[1]+" & "+open_close(dicts,2,"Priest CC")[0]+round_with_padding(dsnop['Priest Control Chance'], 2)+psn['Priest Control Chance']+open_close(dicts,2,"Priest CC")[1]+"   & "+open_close(dicts,2,"Priest CC")[0]+round_with_padding(dmnop['Priest Control Chance'], 2)+pmn['Priest Control Chance']+open_close(dicts,2,"Priest CC")[1]+" & "+open_close(dicts,3,"Priest CC")[0]+round_with_padding(dsrl['Priest Control Chance'], 2)+psl['Priest Control Chance']+open_close(dicts,3,"Priest CC")[1]+"  & "+open_close(dicts,3,"Priest CC")[0]+round_with_padding(dmrl['Priest Control Chance'], 2)+pml['Priest Control Chance']+open_close(dicts,3,"Priest CC")[1]+"        \\\\\n")
            file.write("&                           & & & & &                          & &\\\\\n")
            file.write("&                           & & & & &                          & &\\\\\n")

        file.write("\end{tabular}\n")
        file.write("\end{table}\n")
        print(minim)
        print(maxim)