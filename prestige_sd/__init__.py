from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'prestige_sd'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BC_RATIO = 3
    ENDOWMENT = 100


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    show_payoff = models.BooleanField()
    show_contribution = models.BooleanField()


class Player(BasePlayer):
    contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)

# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    individual_share = group.total_contribution * C.BC_RATIO / len(players)
    for p in players:
        p.payoff = individual_share + C.ENDOWMENT - p.contribution

def generate_others_results_list(player: Player):
    group = player.group
    other_players = player.get_others_in_group()
    res_list = []
    for p in other_players:
        player_dict = {
            "id": p.id_in_group,
            "contribution": p.contribution if group.show_contribution else "？",
            "payoff": p.payoff if group.show_payoff else "？",
        }
        res_list.append(player_dict)
    return res_list


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for g in subsession.get_groups():
            g.show_payoff = g.session.config["show_payoff"]
            g.show_contribution = g.session.config["show_contribution"]

# PAGES
class Decision(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs  


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        player_results = {"payoff": player.payoff, "contribution": player.contribution}
        return {
            'total_contribution': group.total_contribution,
            "player_results": player_results,
            "other_results": generate_others_results_list(player),
            "show_payoff": group.show_payoff,
            "show_contribution": group.show_contribution,
        }   


page_sequence = [Decision, ResultsWaitPage, Results]
