import random
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QPushButton, QStatusBar, QTableWidgetItem
from PyQt5.QtCore import Qt
import sqlite3


class Red:
    # Чем больше число, тем меньше шанс, что бот его выберет
    def run(self):
        a = 1
        b = 0
        while b < 0.3:
            a += 1
            b = random.random()
        return a + 1


class Blue:
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        s = cur.execute("""SELECT number FROM numbers""").fetchall()
        con.close()

        if s:
            d = {}
            for i in s:
                if s.count(i) not in d:
                    d[s.count(i)] = i[0]
            return d[min(list(d.keys()))]
        else:
            return random.randint(1, 10)


class Yellow:
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        s = cur.execute("""SELECT number FROM numbers WHERE bot_id=3""").fetchall()
        con.close()

        if s:
            d = {}
            for i in s:
                if s.count(i) not in d:
                    d[s.count(i)] = i[0]
            return d[min(list(d.keys()))]
        else:
            return random.randint(1, 10)


class Green:
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        s = cur.execute("""SELECT number FROM numbers WHERE win""").fetchall()
        con.close()

        if s:
            d = {}
            for i in s:
                if s.count(i) not in d:
                    d[s.count(i)] = i[0]
            return d[max(list(d.keys()))]
        else:
            return random.randint(1, 10)


class Orange:
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        s = cur.execute("""SELECT number FROM numbers WHERE win AND NOT bot_id=5""").fetchall()
        con.close()

        if s:
            d = {}
            for i in s:
                if s.count(i) not in d:
                    d[s.count(i)] = i[0]
            return d[max(list(d.keys()))]
        else:
            return random.randint(1, 10)


class Purple:
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        s = cur.execute("""SELECT number FROM numbers""").fetchall()
        con.close()

        if s:
            d = {}
            for i in s:
                if s.count(i) not in d:
                    d[s.count(i)] = i[0]
            return int(d[min(list(d.keys()))] * random.random())
        else:
            a = random.randint(1, 10) * random.random() + 1
            return int(a)


class Pink:  # здесь чем чаще число выигрывает - тем чаще его выбирает бот
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        s = cur.execute("""SELECT number FROM numbers WHERE win""").fetchall()

        con.close()

        if s:
            return random.choice(s)
        else:
            return random.randint(1, 10)


class Gray:
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        s = cur.execute("""SELECT number FROM numbers WHERE win""").fetchall()

        con.close()

        n = 0
        while True:
            for i in s:
                for _ in range(100):
                    n += 1
                    a = random.random()
                    if a < 0.1:
                        return i
                    if n >= 100:
                        return random.randint(1, 10)
            return random.randint(1, 10)


class Black:
    def run(self):
        return random.randint(1, 10)


class White:
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        s = cur.execute("""SELECT number FROM numbers WHERE win""").fetchall()
        con.close()

        if s:
            d = {}
            for i in s:
                if s.count(i) not in d:
                    d[s.count(i)] = i
            return d[min(list(d.keys()))]
        else:
            return random.randint(1, 10)


class Brown:
    def run(self):
        """Бот для того, чтобы кому-нибудь приходилось блокировать единицу,
        иначе он всегда будет выигрывать"""

        return 1


class Violet:
    def run(self):
        con = sqlite3.connect("base.db")
        cur = con.cursor()
        k = float(cur.execute('''SELECT k FROM bots WHERE name = "Violet"''').fetchone()[0])
        if cur.execute('''SELECT number FROM numbers WHERE win = True''').fetchall():
            number = int(cur.execute('''SELECT number FROM numbers WHERE win = True''').fetchall()[-1])
        else:
            number = random.randint(1, 5)
        if cur.execute('''SELECT win FROM numbers WHERE bot_id = 1''').fetchall():
            if cur.execute('''SELECT win FROM numbers WHERE bot_id = 1''').fetchall()[-1] != 'True':
                k2 = k - random.random()
                if k2 >= 1:
                    a = 'UPDATE bots set k = "{}" WHERE id = 1'.format(str(k2))
                    cur.execute(a)
                    con.commit()
            con.close()
            a = 0
            while a < 1:
                a = number * k
            return int(a)
        return random.randint(1, 5)


class Game(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("base.db")
        f = open('des.txt', 'r')
        self.des = int(f.read())
        f.close()
        self.run()

    def run(self):
        self.close()
        if self.des == 0:
            uic.loadUi('start1.ui', self)
        else:
            uic.loadUi('start2.ui', self)
        self.pl.clicked.connect(self.game)
        self.stat.clicked.connect(self.show_stat)
        self.change.clicked.connect(self.change_des)
        self.sp.clicked.connect(self.progress)
        self.history.clicked.connect(self.show_history)
        self.show()

    def game(self):
        self.close()
        if self.des == 0:
            uic.loadUi('game1.ui', self)
        else:
            uic.loadUi('game2.ui', self)
        self.back_2.clicked.connect(self.run)
        self.play1.clicked.connect(self.play)
        self.show()

    def play(self):
        self.value = self.spinBox.value()
        bots1 = [self.red, self.blue, self.yellow, self.green,
                 self.orange, self.purple, self.pink, self.gray,
                 self.black, self.white, self.brown, self.violet]
        bots = {}

        self.close()

        if self.des == 0:
            uic.loadUi('play1.ui', self)
        else:
            uic.loadUi('play2.ui', self)
        self.back_3.clicked.connect(self.game)
        cur = self.con.cursor()

        bots_wins = {}

        for i in range(len(bots1)):
            if bots1[i].isChecked():
                bots[bots1[i].text()] = [0]
                if bots1[i].text() == 'Red':
                    bots['Red'].append(Red())
                elif bots1[i].text() == 'Blue':
                    bots['Blue'].append(Blue())
                elif bots1[i].text() == 'Yellow':
                    bots['Yellow'].append(Yellow())
                elif bots1[i].text() == 'Green':
                    bots['Green'].append(Green())
                elif bots1[i].text() == 'Orange':
                    bots['Orange'].append(Orange())
                elif bots1[i].text() == 'Purple':
                    bots['Purple'].append(Purple())
                elif bots1[i].text() == 'Pink':
                    bots['Pink'].append(Pink())
                elif bots1[i].text() == 'Gray':
                    bots['Gray'].append(Gray())
                elif bots1[i].text() == 'Black':
                    bots['Black'].append(Black())
                elif bots1[i].text() == 'White':
                    bots['White'].append(White())
                elif bots1[i].text() == 'Brown':
                    bots['Brown'].append(Brown())
                elif bots1[i].text() == 'Violet':
                    bots['Violet'].append(Violet())

                bots_wins[bots1[i].text()] = 0
                bots[bots1[i].text()].append(0)

        for i in range(self.value):
            for bot in bots:
                bot1 = bots[bot][1]
                bots[bot][2] = bot1.run()

                games = 'SELECT games FROM bots WHERE name = "{}"'.format(bot)

                a = 'UPDATE bots SET games = {} WHERE name = "{}"'.format(
                    str(int(cur.execute(games).fetchone()[0]) + 1), bot)

                cur.execute(a)
                self.con.commit()

            win_bot = ''

            values = [int(bots[bot][2]) for bot in bots]

            while values and values.count(min(values)) > 1:
                a = min(values)
                while a in values:
                    values.remove(a)

            if values:
                win_value = min(values)
                for bot in bots:
                    if int(bots[bot][2] == win_value):
                        win_bot = bot

            for bot in bots:
                bot_id = 'SELECT id FROM bots WHERE name = "{}"'.format(bot)

                a = 'INSERT INTO numbers(number, win, bot_id) VALUES({}, "{}", {})'.format(str(bots[bot][2]),
                str(bot == win_bot),
                                                  str(cur.execute(bot_id).fetchone()[0]))
                if bot == win_bot:
                    bots_wins[bot] += 1

                cur.execute(a)

        a = ''

        for bot in bots_wins:
            a = a + str(bot) + ': ' + str(bots_wins[bot]) + ' побед' + '\n'
            wins = 'SELECT win_games FROM bots WHERE name = "{}"'.format(bot)

            s = 'UPDATE bots SET win_games = {} WHERE name = "{}"'.format(
                    str(int(cur.execute(wins).fetchone()[0]) + bots_wins[bot]), bot)

            cur.execute(s)
            self.con.commit()

        self.label.setText(a)
        self.con.commit()

        self.show()

    def show_stat(self):
        self.close()
        if self.des == 0:
            uic.loadUi('stat1.ui', self)
        else:
            uic.loadUi('stat2.ui', self)
        cur = self.con.cursor()
        s = cur.execute('''SELECT name, games, win_games FROM bots''').fetchall()
        self.table.setRowCount(len(s))
        self.table.setColumnCount(len(s[0]))
        self.titles = [description[0] for description in cur.description]
        self.table.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(s):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.back.clicked.connect(self.run)
        self.show()

    def change_des(self):
        self.des = (self.des + 1) % 2

        f = open('des.txt', 'w')
        f.write(str(self.des))
        f.close()

        self.run()

    def progress(self):
        cur = self.con.cursor()
        a = [i[0] for i in cur.execute('''SELECT name FROM bots''').fetchall()]

        for bot in a:
            s = 'UPDATE bots SET games = 0 WHERE name = "{}"'.format(bot)
            cur.execute(s)
            s = 'UPDATE bots SET win_games = 0 WHERE name = "{}"'.format(bot)
            cur.execute(s)

        cur.execute('UPDATE bots SET k = "1.5" WHERE id = 12')
        self.con.commit()

        cur.execute('''DELETE FROM numbers''')
        self.con.commit()
        self.run()
    
    def show_history(self):
        self.close()
        if self.des == 0:
            uic.loadUi('stat1.ui', self)
        else:
            uic.loadUi('stat2.ui', self)
        cur = self.con.cursor()
        s = cur.execute('''SELECT * FROM numbers''').fetchall()
        self.table.setRowCount(len(s))
        self.table.setColumnCount(len(s[0]))
        self.titles = [description[0] for description in cur.description]
        self.table.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(s):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.back.clicked.connect(self.run)
        self.show()



app = QApplication(sys.argv)
g = Game()
sys.exit(app.exec_())
