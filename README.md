# myersoncoop

Compute the Myerson Values (Shapleys on a graph) of both the Policy and stats of a 3v3 "arena" game.

# Game Description
This game is inspired by World of Warcraft 3v3 arenas.

Two teams made by a Warrior, a Mage and a Priest fight each other.

The teams perform their sequence of actions by turn.

At the beginning of each fight, one team is chosen to start first.

The priority of action in every team is the following: 1) Warrior, 2) Mage, 3) Priest

## Victory condition
The game ends when all the players in a team are dead.

# Role Description
Every player has a **_policy_** and a set of stats:
1. Max HP
2. Attack Power
3. Healing Power
4. Control Chance
## Warrior
The warrior can only _attack_ an enemy player.

He damages the enemy by an amount equal to his **Attack Power**.
## Mage
A mage can only _control_ (put to sleep) an enemy player.

His chance of controlling the enemy is equal to his **Control Chance**  * (1 + **Attack Power**/20)

When an enemy player is put to sleep he can not perform any action during the next turn.

## Priest
A priest can only _heal_ a teammate.

He heals the teammate by an amount equal to his **Healing Power**

# Policies
Two different policies are enabled: 1) Random 2) Smart.

## Random Policy
With this policy the target of the warrior and the mage are uniformly chosen between the alive enemies.
The target of the priest is chosen between the alive teammates.

## Smart Policy
The Warrior and Mage target the enemies with this priority list: 1) Priest, 2) Mage, 3) Warrior
The Priest always heals the teammate with the least HP.

# Experiment Setup
The Mayerson Values for the following characteristics are computed:
1. Warrior Max HP
2. Warrior Policy
3. Warrior Attack Power
4. Warrior Healing Power
5. Warrior Control Chance
6. Mage Max HP
7. Mage Policy
8. Mage Attack Power
9. Mage Healing Power
10. Mage Control Chance
11. Priest Max HP
12. Priest Policy
13. Priest Attack Power
14. Priest Healing Power
15. Priest Control Chance

When a characteristic is not present in a coalition it is put to 0.
When a policy is not present in a coalition the agent does not perform any action.

## Shapley vs Myerson
Computing the Shapley Values for this set of characteristics is already computationally expensive given the huge number
of possible coalitions.

But knowing a-priori something about the structure of the game allows us to build up a graph and to compute the Myerson
values on this graph. Note that in order to compute the Meyerson values you sum the utility functions of every **_connected_**
components in a coalition. This greatly reduces the complexity of the approach.

## The graph for this problem
Since when the player max HP is put to 0 he is dead and when the policy is not present the player does not act, we can
build the following graph for the game:
![alt text](graph.png "Graph")

It is clear that when one the Max HP of a player is not in a coalition, all the branch linked to it do not contribute to
the coalition utility (the same works for the Policy).

## Simulations
We compute the Myerson Values for the first team of an Arena where the first team acts with a Smart Policy and the second
team with a Random Policy.

The Myerson Values are computed with the Montecarlo Sampling Approximation taken from https://arxiv.org/abs/2001.00065

but actually there are so few different connected coalitions that an exact calculation is not so expensive.

## Results
The results are provided in hybrid_results.json and here:
1. "Warrior Max HP": 19.720561079486124
2. "Warrior Policy": 0.6382521207398747
3. "Warrior Attack Power": 0.6366533135144863
4. "Warrior Healing Power": -0.004131176548843827
5. "Warrior Control Chance": 0.001546824696879214
6. "Mage Max HP": 19.716973139166672
7. "Mage Policy": 0.13344323139868602
8. "Mage Attack Power": 0.03269830517974558
9. "Mage Healing Power": -0.00046144266976715103
10. "Mage Control Chance": 0.10901688699375713
11. "Priest Max HP": 17.962603541120533
12. "Priest Policy": 0.6612162217739637
13. "Priest Attack Power": 0.0020078791985821535
14. "Priest Healing Power": 0.660030789862061
15. "Priest Control Chance": 0.0035148832165688014

### Discussion
As expected the most important stats are the Max HP.
The second most important stats are the Policies.

Since the warrior policy entirely depends on his attack power, the attack power myerson value is almost identical to the policy one.
The myerson values of other warrior stats are almost zero.

Since the mage policy depends on the control chance and on the attack power, their meyerson value are the only one within the set
of stats that are statistically different from zero.

Since the priest policy only depends on his healing power, the healing power myerson value is almost identical to the policy one.
The other values are almost zero.

## Copyright
Copyright 2022 Giorgio Angelotti


