# -*- coding: utf-8 -*-
import config
import gui
import lesson
import sched
import time


class App:
    def __init__(self):
        self.cfg = config.Config('config.json').get_dic()
        self.card_wnd = gui.CardWindow()
        self.card_wnd.bind('on_return', self.check_answer)
        self.card_wnd.bind('on_destroy', self.on_destroy)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.ask_for_start()
        self.card_wnd.mainloop()

    def on_destroy(self):
        dlg = gui.CloseDialog(self.card_wnd.root)
        if dlg.result == 0:
            self.hide_for_timeout()
        elif dlg.result == 1:
            self.lesson.end_lesson()
            self.card_wnd.root.quit()

    def ask_for_start(self):
        self.lesson = lesson.Lesson(self.cfg)
        self.status = 'ask_for_start'
        d = self.lesson.direction
        w = u'Ready to start?' if (d == 'ru-en') else u'Готовы начать?'
        t = u'Print "Go!" then' if (d == 'ru-en') else u'Тогда введите "Да!"'
        self.card_wnd.set_input(w, t, 0)
        self.card_wnd.set_history([])
        self.card_wnd.show()

    def run_lesson(self):
        self.lesson.set_new_card()
        self.after_repeat = False
        quest, trans, answ, d = self.lesson.get_current()
        percent = self.lesson.current_card.statistic[d].percent
        if d == 'ru-en':
            trans = ''
        history = self.lesson.current_card.statistic[d].history
        self.card_wnd.set_history(history)
        self.card_wnd.set_input(quest, trans, percent)
        self.set_left()
        self.card_wnd.show()

    def check_answer(self, answer):
        answer = answer.lower().strip()
        if self.status == 'ask_for_start':
            if answer == u'go!' or answer == u'да!':
                self.status = 'waiting_for_answer'
                self.run_lesson()
        elif self.status == 'waiting_for_answer':
            if self.lesson.check_answer(answer, not self.after_repeat):
                self.set_right_answer()
                self.status = 'continue'
            else:
                self.set_wrong_answer()
                self.status = 'repeat'
            self.after_repeat = False
        elif self.status == 'repeat':
            self.set_repeat()
            self.after_repeat = True
            self.status = 'waiting_for_answer'
        elif self.status == 'continue':
            self.status = 'waiting_for_answer'
            if not self.lesson.is_end():
                self.run_lesson()
            else:
                self.hide_for_timeout()

    def set_wrong_answer(self):
        quest, trans, answ, d = self.lesson.get_current()
        percent = self.lesson.current_card.statistic[d].percent
        if d == 'ru-en':
            answ += ' ' + trans
        history = self.lesson.current_card.statistic[d].history
        self.card_wnd.set_history(history)
        self.card_wnd.set_wrong_answer(answ, percent)

    def set_repeat(self):
        quest, trans, answ, d = self.lesson.get_current()
        percent = self.lesson.current_card.statistic[d].percent
        if d == 'ru-en':
            trans = ''
        history = self.lesson.current_card.statistic[d].history
        self.card_wnd.set_history(history)
        self.card_wnd.set_repeat(quest, trans, percent)

    def set_right_answer(self):
        quest, trans, answ, d = self.lesson.get_current()
        percent = self.lesson.current_card.statistic[d].percent
        if d == 'ru-en':
            answ += ' ' + trans
        history = self.lesson.current_card.statistic[d].history
        self.card_wnd.set_history(history)
        self.card_wnd.set_right_answer(answ, percent)

    def set_left(self):
        total = len(self.lesson.cards) + 1
        done = self.lesson.right_answer_counter
        left = min(self.cfg['cards_per_lesson'] - done, total)
        self.card_wnd.set_left('%d/%d' % (left, total))

    def hide_for_timeout(self):
        self.lesson.end_lesson()
        self.card_wnd.hide()
        self.scheduler.enter(self.cfg['retry_time_sec'], 1,
                             self.ask_for_start, ())
        self.scheduler.run()
