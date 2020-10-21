import numpy as np
import pygame
import pygame.draw as pgd
from random import randint
from tkinter import Tk
from tkinter.messagebox import showerror, showinfo
pygame.init()

X, Y = (1200, 900)
FPS = 30
screen = pygame.display.set_mode((X, Y))

COLOR = {  #Словарь цветов
'Orange' : (255, 178,   0),
'SkyBlue': (135, 206, 235),
'Pink'   : (255,  20, 147),
'Blue'   : (  0,   0, 139),
'Red'    : (255,   0,   0),
'Maroon' : (128,   0,   0),
'White'  : (255, 255, 255),
'Black'  : (  0,   0,   0)}

_color_key = ('Orange', 'SkyBlue', 'Pink', 'Blue',
              'Red', 'Maroon', 'White', 'Black')  #Служебный кортеж цыетов


def set_color(num: int):
    '''
    Возвращает цвет по номеру-ключу.
    ----------------------------------------------------------
    num - номер-ключ
    '''
    return COLOR[_color_key[num]]


def rand_sign():
    '''
    С равной вероятностью возвращает 1 или -1.
    '''
    return (-1)**randint(0, 1)


def kenny_figure(surface, color, X0, R, angles):
    '''
    Рисует правильный многоугольник с заданными количеством углов, цветом
    и расстоянием от центра до вершины на заданной поверхности.
    ----------------------------------------------------------
    surface - поверхность рисования
    color - цвет
    X0 - кортеж координат центра фигуры
    R - расстояние от центра до вершин
    angles - количество углов
    '''
    x0, y0 = X0
    X = []
    for i in range(angles):
        x = R * np.exp(-1j * 2*np.pi/angles * i).real
        y = R * np.exp(-1j * 2*np.pi/angles * i).imag
        X.append([x + x0, y + y0])
    pgd.polygon(surface, color, X)


class Ball ():
    '''
    Класс цветных шариков, которые могут двигаться и отражаться от стенок.
    '''
    def __init__(self, surface, R: int, color: tuple, X0: tuple,
                 V0: tuple, name: str = 'ball'):
        '''
        surface - поверхность рисования шарика
        R - радиус шарика
        color - цвет шарика
        X0 - координаты шарика
        V0 - скорости шарика
        name - имя шарика
        '''
        self.surface = surface
        self.R = R
        self.color = color
        self.X = np.array(X0)
        self.V = np.array(V0)
        self.name = name

    def move(self, dt):
        '''
        Изменяет координаты шарика за указанный период времени исходя из его
        положения и скорости.
        ----------------------------------------------------------
        dt - промежуток времени, в ходе которого движение линейно
        '''
        if self.X[0] + self.V[0] * dt >= X or self.X[0] + self.V[0] * dt <= 0:
            self.V[0] = -self.V[0]
            self.V[1] += rand_sign() * randint(0, 15)
        if self.X[1] + self.V[1] * dt >= Y or self.X[1] + self.V[1] * dt <= 0:
            self.V[1] = -self.V[1]
            self.V[0] += rand_sign() * randint(0, 15)

        self.X = self.X + self.V * dt

    def show(self):
        '''
        Рисует шарик или многоугольник, если имя - Кенни.
        '''
        if self.name == 'Kenny':
            kenny_figure(self.surface, self.color, self.X, self.R, 7)
        else:
            pgd.circle(self.surface, self.color, (int(self.X[0]),
                                                  int(self.X[1])), self.R)


class Balls ():
    '''
    Класс групп шариков Ball, фактически обёртка для Ball, позволяющая коротко
    реализовать множественность объектов Ball.
    '''
    def __init__(self, surface, balls: np.ndarray):
        '''
        surface - поверхность рисования шариков
        balls - массив с объектами Ball
        '''
        self.balls = balls

    def move(self, dt):
        '''
        Изменяет координаты шариков за указанный период времени исходя из их
        положений и скоростей.
        ----------------------------------------------------------
        dt - промежуток времени, в ходе которого движение линейно
        '''
        for i in self.balls:
            i.move(dt)

    def show(self):
        '''
        Рисует каждый объект из balls
        '''
        for i in self.balls:
            i.show()


def init_balls(Number, R_max, kenny_chance=10):
    '''
    Создаёт массив с объектами balls со случайными параметрами, которые
    можно ограничить.
    ----------------------------------------------------------
    Number - количество шариков
    R_max - максимальный радиус шарика (минимальный - 5)
    kenny_chance - обратная вероятность создания шарика с именем "Кенни"
    '''
    standart = Ball(screen, 20, COLOR['SkyBlue'], (600, 450),
                    (20, 20), name='Lilith')

    balls = np.array([standart])

    for i in range(Number):
        R = randint(5, R_max)
        X0 = (randint(0, X), randint(0, Y))
        V0 = (rand_sign()*randint(60, 250), rand_sign()*randint(60, 250))
        if randint(0, kenny_chance) == 10:
            balls = np.append(balls, Ball(screen, R,
                              set_color(randint(0, len(COLOR) - 2)), X0,
                              V0, name='Kenny'))
        else:
            balls = np.append(balls, Ball(screen, R,
                              set_color(randint(0, len(COLOR) - 2)), X0,
                              V0, name='ball {}'.format(i)))
    balls = np.delete(balls, 0)
    return balls


def click(event, kit: Balls):
    '''
    Обрабатывает событие нажатия кнопки мыши, удаляя шарик, если на него
    нажали и добавляя новый - случайный; возвращает количество набранных
    очков.
    ----------------------------------------------------------
    event - событие pygame
    kit - группа шариков Balls
    '''
    points = 0
    x_m, y_m = event.pos
    for i in kit.balls:
        x, y = i.X
        if (x - x_m) ** 2 + (y - y_m) ** 2 <= i.R ** 2:
            if i.name == 'Kenny':
                points += -5
                root = Tk()
                root.withdraw()
                showerror(title="Господи, они убили Кенни!",
                          message="Сволочи!")
                root.destroy()
            else:
                points += 1
            kit.balls = np.append(kit.balls, init_balls(1, 50))
            pos = kit.balls.tolist().index(i)
            kit.balls = np.delete(kit.balls, pos)
            break
    return points


def insert(name, points):
    '''
    Записывает в файл Leader Board.txt результат игры и возвращает место
    в рейтинге игроков.
    ----------------------------------------------------------
    name - имя игрока
    points - счёт игрока
    '''
    file = open('Leader Board.txt', 'r')
    M = np.array([], dtype=str)
    scores = np.array([], dtype=int)
    for s in file:
        M = np.append(M, s)
        num = ''
        for sym in s:
            try:
                num += str(int(sym))
            except ValueError:
                continue
        scores = np.append(scores, int(num))
    file.close()

    pos = 0
    for i in range(np.size(scores)):
        if scores[i] <= points:
            scores = np.insert(scores, i, points)
            pos = i
            break
    newstr = '{} :: {} \n'.format(name, points)
    M = np.insert(M, pos, newstr)
    print(M)

    file = open('Leader Board.txt', 'w')
    file.writelines(M)
    return pos+1
