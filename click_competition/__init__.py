import time

from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = "click_competition"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    clicks = models.IntegerField(initial=0)


# PAGES
class ClickPage(Page):
    timeout_seconds = 10

    @staticmethod
    def vars_for_template(player: Player):
        my_id = player.id_in_group
        opponent_id = C.PLAYERS_PER_GROUP - my_id + 1
        return {"my_id": my_id, "opponent_id": opponent_id}

    @staticmethod
    def js_vars(player: Player):
        return {"start_time": time.time()}

    @staticmethod
    def live_method(player: Player, data):
        if data.get("action") == "click":
            player.clicks += 1

        all_clicks = {p.id_in_group: p.clicks for p in player.group.get_players()}

        return {0: all_clicks}


class Results(Page):
    # def is_displayed(self):
    #     return self.round_number == C.NUM_ROUNDS
    pass


page_sequence = [ClickPage]
