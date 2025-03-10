from otree.api import BaseConstants, BasePlayer

def num_of_coopeartors(C: BaseConstants, players: BasePlayer):
    return sum([C.DECITION_DICT[p.decision] for p in players])

def caluculate_payoff(C: BaseConstants, players: BasePlayer):
    num_cooperators = num_of_coopeartors(C, players)
    total_players = len(players)

    return num_cooperators * C.BC_RATIO / total_players

