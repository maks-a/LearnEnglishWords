# -*- coding: utf-8 -*-
import Tkinter as tk
import tkFont
import tkSimpleDialog

clr_stat_frame = '#EEFFFF'
clr_word_frame = '#FFFFEE'
clr_answer_frame = '#EEFFFF'
clr_success = '#338800'
clr_error = '#FF0033'
clr_black = '#000000'
clr_tbl_bg = ['#EEFFFF', '#FFFFEE']
clr_stat = ['#777700', '#007700', '#777777']


class CloseDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        self.var = tk.IntVar(0)
        tk.Radiobutton(master, text='Close current lesson', variable=self.var,
                       value=0).grid(sticky="w")
        tk.Radiobutton(master, text='Close programm', variable=self.var,
                       value=1).grid(sticky="w")
        self.resizable(False, False)
        return None

    def apply(self):
        self.result = self.var.get()


class PieChart(tk.Frame):
    def __init__(self, parent, d=20, bg=clr_stat_frame, bd=0):
        tk.Frame.__init__(self, parent, bg=bg, bd=bd)
        self.root = parent

        self.d = d
        self.canvas = tk.Canvas(self, width=d, height=d, highlightthickness=0,
                                bg=clr_stat_frame)
        self.canvas.pack()

    def calculate(self, percent):
        self.canvas.delete('all')
        xy = 1, 1, self.d - 1, self.d - 1
        ex = -359 * percent / 100
        self.canvas.create_arc(xy, start=90, extent=ex, fill='gray',
                               outline='gray')
        self.canvas.create_arc(xy, start=90, extent=359, fill='',
                               outline='gray')
        self.canvas.update()


class HistoryBar(tk.Frame):
    def __init__(self, parent, bg=clr_stat_frame, bd=0):
        tk.Frame.__init__(self, parent, bg=bg, bd=bd)
        self.root = parent

        history_len = 20
        self.elem_num = history_len
        self.elem_width = 9
        self.elem_height = 4
        w = self.elem_width * self.elem_num + 1
        h = self.elem_height
        self.canvas = tk.Canvas(self, width=w, height=h, bg='white')
        self.canvas.pack()

    def calculate(self, data):
        self.canvas.delete('all')
        n = self.elem_num
        w = self.elem_width
        h = self.elem_height
        x = 1
        d = [2] * (n - len(data)) + data
        for i in d:
            color = 'gray'
            if i == 0:
                color = 'red'
            elif i == 1:
                color = 'green'
            self.canvas.create_rectangle(x, 1, x + w, h, fill=color,
                                         outline='white')
            x += w
        self.canvas.update()


class CardWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.callbacks = {}
        self.show_answer = True
        self.init_window()

    def mainloop(self):
        if self.callbacks['on_destroy'] == None:
            self.root.quit()
        else:
            self.root.mainloop()

    def bind(self, event, func):
        self.callbacks[event] = func

    def init_window(self):
        self.font_main = tkFont.Font(family='Arial', size=12)
        self.font_error = tkFont.Font(family='Arial', size=12, overstrike=1)
        #---
        frame_stat = tk.Frame(self.root, bg=clr_stat_frame, bd=5)
        frame_stat.pack(fill='both')
        self.pie_chart = PieChart(frame_stat, bd=10)
        self.pie_chart.pack(side='right')
        self.history_bar = HistoryBar(frame_stat, bd=10)
        self.history_bar.pack(side='right')
        self.label_left = tk.Label(frame_stat, bg=clr_stat_frame, bd=10)
        self.label_left.pack(side='left')

        #---
        frame_word = tk.Frame(self.root, bg=clr_word_frame, bd=5)
        frame_word.pack(fill='both')
        self.label_word = tk.Label(frame_word, bg=clr_word_frame)
        self.label_word.pack()

        frame_transcription = tk.Frame(self.root, bg=clr_word_frame, bd=5)
        frame_transcription.pack(fill='both')
        self.label_transcription = tk.Label(frame_transcription,
                                            bg=clr_word_frame)
        self.label_transcription.pack()

        #---
        frame_answ = tk.Frame(self.root, bg=clr_answer_frame, bd=15)
        frame_answ.pack(fill='both')

        frame_message = tk.Frame(frame_answ, bg=clr_answer_frame)
        frame_message.pack(fill='both')

        self.label_message = tk.Label(frame_message, bg=clr_answer_frame)
        self.label_message.pack()

        self.entry_answer = tk.Entry(frame_answ, width=30, justify='center')
        self.entry_answer.pack(side='bottom')
        self.entry_answer.focus()

        #---
        #self.root.bind('<Return>', self.return_pressed)
        self.root.bind('<Return>', self.on_return)
        #self.bind('<FocusIn>', lambda event: self.entry_answer.focus())
        #---
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.title('Learing English Words')
        self.root.resizable(False, False)
        self.root.wm_geometry('+%d+%d' % (x, y))
        self.root.protocol('WM_DELETE_WINDOW', self.on_destroy)
        #self.font = tkFont.Font(family='Arial')

    def set_input(self, word, transcription, percent):
        self.pie_chart.calculate(percent)
        self.label_word['text'] = word
        self.label_transcription['text'] = transcription
        self.label_message['text'] = ''
        self.entry_answer['fg'] = clr_black
        self.entry_answer['state'] = 'normal'
        self.entry_answer.delete(0, tk.END)
        self.entry_answer['font'] = self.font_main

    def set_right_answer(self, right_answer, percent):
        self.pie_chart.calculate(percent)
        self.label_message['fg'] = clr_success
        self.label_message['text'] = right_answer
        self.entry_answer['state'] = 'readonly'
        self.entry_answer['font'] = self.font_main

    def set_wrong_answer(self, right_answer, percent):
        self.pie_chart.calculate(percent)
        self.set_right_answer(right_answer, percent)
        self.entry_answer['fg'] = clr_error
        self.entry_answer['font'] = self.font_error

    def set_repeat(self, word, transcription, percent):
        self.pie_chart.calculate(percent)
        self.set_input(word, transcription, percent)
        self.label_message['fg'] = clr_error
        self.label_message['text'] = 'Повторим еще раз'

    def set_history(self, history):
        self.history_bar.calculate(history)

    def set_left(self, left):
        self.label_left['text'] = left

    def on_return(self, event):
        user_answer = self.entry_answer.get()
        self.callbacks['on_return'](user_answer)

    def on_destroy(self):
        self.callbacks['on_destroy']()

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.deiconify()
        self.entry_answer.focus()

###############################################
#EN-RU
def look_1(card_wnd):
    card_wnd.set_history([0,1,0,1,1])
    card_wnd.set_input('aback', '[əbˈæk]', 30)
def look_2(card_wnd):
    card_wnd.set_history([0,1,0,1,1,0])
    card_wnd.set_wrong_answer('захваченный врасплох, смущенный', 20)
def look_3(card_wnd):
    card_wnd.set_history([0,1,0,1,1,0])
    card_wnd.set_repeat('aback very very very very long word', '[əbˈæk]', 20)
def look_4(card_wnd):
    card_wnd.set_history([0,1,0,1,1,0,1])
    card_wnd.set_right_answer('захваченный врасплох, смущенный', 30)
#RU-EN
def look_5(card_wnd):
    card_wnd.set_history([0,1,0,1,1,0,1,1])
    card_wnd.set_input('уничтожать, отменять, упразднять, аннулировать',
                       '', 20)
def look_6(card_wnd):
    card_wnd.set_history([0,1,0,1,1,0,1,1,0])
    card_wnd.set_wrong_answer('aback'+' [əbˈæk]',10)
def look_7(card_wnd):
    card_wnd.set_history([0,1,0,1,1,0,1,1,0])
    card_wnd.set_repeat('захваченный врасплох, смущенный', '',10)
def look_8(card_wnd):
    card_wnd.set_history([0,1,0,1,1,0,1,1,0,1])
    card_wnd.set_right_answer('aback'+' [əbˈæk]',20)
def look_9(card_wnd):
    print 'run look_9'
    card_wnd.hide()
    import sched
    import time
    s = sched.scheduler(time.time, time.sleep)
    def handler():
        print 'handler'
        card_wnd.show()
        look_1(card_wnd)
        print 'handler end'
    s.enter(3, 1, handler, ())
    s.run()


current_look = 1
looks = {
    1: look_1,
    2: look_2,
    3: look_3,
    4: look_4,
    5: look_5,
    6: look_6,
    7: look_7,
    8: look_8,
    9: look_9
}

wnd = 0


def change_look(answer):
    global current_look
    global looks
    global wnd
    current_look += 1
    if current_look > len(looks):
        current_look = 1
    looks[current_look](wnd)


def main():
    card_wnd = CardWindow()
    card_wnd.bind('on_return', change_look)
    global looks
    global wnd
    wnd = card_wnd
    looks[current_look](wnd)
    card_wnd.mainloop()


if __name__ == '__main__':
    main()
