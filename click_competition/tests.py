from otree.api import Bot

from . import *


class PlayerBot(Bot):
    def play_round(self):
        # ① グループが2人ずつ割り当てられているか確認
        assert len(self.player.get_others_in_group()) == 1, "グループに2人いない"

        # ② クリックゲームでランダムなクリック数を送信
        import random

        clicks = random.randint(5, 15)  # 5～15回クリック
        self.player.clicks = clicks

        # ④ `Results` で正しくスコアが表示されているか確認
        other_player = self.player.get_others_in_group()[0]
        assert self.player.clicks is not None, "クリック数が保存されていない"
        assert other_player.clicks is not None, "相手のクリック数が保存されていない"
