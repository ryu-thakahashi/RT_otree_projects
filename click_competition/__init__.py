import time

from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = "click_competition"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 100
    TIME_LIMIT = 5
    COUNTDOWN_TIME = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    show_opponent = models.BooleanField()  # 相手のクリック数が見える条件か否か

    def set_treatment(group: BaseGroup):
        group.show_opponent = True if group.id_in_subsession % 2 == 0 else False

    winner_id = models.IntegerField()  # 勝者の ID を記録
    tie = models.BooleanField()  # 引き分けなら True

    def set_winner(group: BaseGroup):
        """勝者を決定"""
        group.tie = False
        p1, p2 = group.get_players()
        if p1.clicks == p2.clicks:
            group.tie = True

        if p1.clicks > p2.clicks:
            group.winner_id = p1.id_in_group
        elif p1.clicks < p2.clicks:
            group.winner_id = p2.id_in_group


class Player(BasePlayer):
    clicks = models.IntegerField(initial=0)


# PAGES
class WaitForStart(WaitPage):
    group_by_arrival_time = True
    body_text = "他のプレイヤーを待っています。"
    after_all_players_arrive = Group.set_treatment  # 全員が揃ったら処理を実行


class ClickPage(Page):
    timeout_seconds = C.TIME_LIMIT + C.COUNTDOWN_TIME

    @staticmethod
    def vars_for_template(player: Player):
        res_dict = {}
        res_dict["my_id"] = player.id_in_group
        res_dict["opponent_id"] = C.PLAYERS_PER_GROUP - res_dict["my_id"] + 1
        res_dict["show_opponent"] = player.group.show_opponent

        res_dict["game_time"] = C.TIME_LIMIT
        res_dict["countdown_time"] = C.COUNTDOWN_TIME

        return res_dict

    @staticmethod
    def js_vars(player: Player):
        return {"start_time": time.time()}

    @staticmethod
    def live_method(player: Player, data):
        if data.get("action") == "click":
            player.clicks += 1

        all_clicks = {p.id_in_group: p.clicks for p in player.group.get_players()}

        return {0: all_clicks}


class WaitForAll(WaitPage):
    after_all_players_arrive = Group.set_winner  # 全員が揃ったら勝者を決定


class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        opponent = player.get_others_in_group()[0]
        group = player.group
        reslt = (
            "引き分け"
            if group.tie
            else "勝ち！" if group.winner_id == player.id_in_group else "負け"
        )
        return {
            "my_clicks": player.clicks,
            "opponent_clicks": opponent.clicks,
            "result": reslt,
        }

    pass


page_sequence = [WaitForStart, ClickPage, WaitForAll, Results]
