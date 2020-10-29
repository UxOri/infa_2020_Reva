from random import randrange as rnd, choice
import tkinter as tk
import numpy as np
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class target():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.x = rnd(400, 780)
        self.y = rnd(300, 650)
        self.r = rnd(20, 80)
        self.id = canv.create_oval(0, 0, 0, 0)
        self.id_points = canv.create_text(30, 30, text=self.points, font='28')
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x
        y = self.y
        r = self.r
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)
        
    def re_init(self):
        self.x = rnd(400, 780)
        self.y = rnd(300, 650)
        self.r = rnd(20, 80)

class ball():
    def __init__(self, x=40, y=450, g=3):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.g = g
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self, dt):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= self.g*dt
        self.x += self.vx * dt
        self.y += -self.vy * dt

    def hittest(self, obj: target):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5 <= self.r + obj.r:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.balls = []
        self.bullet = 0
        self.id = canv.create_line(20, 450, 50, 420, width=7) # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.bullet += 1
        new_ball = ball()
        self.an = np.arctan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * np.cos(self.an)
        new_ball.vy = - self.f2_power * np.sin(self.an)
        self.balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = np.arctan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * np.cos(self.an),
                    450 + max(self.f2_power, 20) * np.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


t1 = target()
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()

def new_game(event=''):
    t1.new_target()
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    t1.live = 1
    while t1.live:
        for b in g1.balls:
            b.move(1)
            b.set_coords()
            if b.hittest(t1) and t1.live:
                canv.delete(b.id)
                b.x = 1000
                t1.live = 0
                t1.hit()
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1,
                                text='Вы уничтожили цель за {} выстрелов'.format(g1.bullet))
                canv.update()
                time.sleep(1)
                g1.bullet = 0
                #b.delete
                canv.delete(t1)
                t1.re_init()
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(g1)
    root.after(750, new_game)


new_game()

tk.mainloop()
