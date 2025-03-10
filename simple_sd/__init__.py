from otree.api import *
from simple_sd.payoff_caluculator import num_of_coopeartors, caluculate_payoff

doc = """
Simple Social Dilemma Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'simple_sd'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    BC_RATIO = 3
    DECITION_DICT = {"Cooperate": 1, "Defect": 0}


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.session.config.get("players_per_group"):
            self.session.config["players_per_group"] = C.PLAYERS_PER_GROUP  


class Group(BaseGroup):
    def set_payoffs(group: BaseGroup):
        players = group.get_players()
        for p in players:
            p.payoff = caluculate_payoff(C, players)

class Player(BasePlayer):
    decision = models.StringField(
        choices=['Cooperate', 'Defect'],
        widget=widgets.RadioSelectHorizontal,
        doc="""Whether the player cooperates (True) or defects (False)"""
    )


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = Group.set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group_players = player.get_others_in_group()
        num_cooperators = num_of_coopeartors(C, group_players)
        return {
            "player": player,
            "group_players": group_players,
            "num_cooperators": num_cooperators,
            "total_players": len(group_players),
            "payoff": player.payoff
        }


page_sequence = [MyPage, ResultsWaitPage, Results]
