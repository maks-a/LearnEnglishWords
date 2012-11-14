# -*- coding: utf-8 -*-
import card
import json
import json_com
import random


class Dictionary:
    def __init__(self, cfg_dic):
        self.cfg = cfg_dic
        self.reload()
        self.save()

    def reload(self):
        raw_dic = json_com.parse(self.cfg['path_to_dict'])
        stat = json_com.parse(self.cfg['path_to_stat'])
        self.cards = set()
        for en_word, transcription, ru_words in raw_dic:
            c = card.Card(en_word, transcription, ru_words.split(','))
            if en_word in stat:
                c.unpack(stat[en_word])
            self.cards.add(c)

    def save(self):
        stat_json = {}
        for c in self.cards:
            percent = (c.statistic['en-ru'].percent +
                       c.statistic['ru-en'].percent)
            if percent > 0:
                stat_json[c.get_en_word()] = c.pack()
        json.dump(stat_json, open(self.cfg['path_to_stat'], 'wb'), indent=2)

    def get_lesson_cards(self):
        def comp(c):
            stat = c.statistic
            rating = (stat['en-ru'].percent + stat['ru-en'].percent) / 2
            random.seed()
            if 0 < rating < 100:
                return (1, random.randrange(1, 10))
            elif rating == 0:
                return (2, random.randrange(1, 10))
            else:
                return (3, random.randrange(1, 10))
        dic = sorted(self.cards, key=comp)
        study_cards_num = self.cfg['study_cards_num']
        return dic[:study_cards_num]
