import numpy as np
import pygame
import pygame.draw as pgd

'''Размер окна и горизонт'''
X = 600
Y = 900
Horizon = 450
screen = pygame.display.set_mode((X, Y))

'''Цвета'''
BLACK_COLOR         =  (  0,   0,   0)
SKY_COLOR           =  (110, 110, 110)
GROUND_COLOR        =  (110, 133, 129)
CAR_COLOR = {'BODY'  : (117, 199, 214),
             'WINDOW': (188, 212, 212),
             'WHEEL' : ( 49,  79,  84)}
CITY_COLOR          = ((183, 200, 196),
                       (200, 213, 210),
                       (147, 172, 167),
                       (175, 192, 194),
                       (120, 152, 145))

def background ():
    '''
    Рисует небо и землю, разделяя их на горизонте.
    -------------------------------------
    '''
    pgd.rect(screen, SKY_COLOR, (0, 0, X, Y))
    pgd.rect(screen, GROUND_COLOR, (0, Horizon, X, Y/2))
        
def building (x, y, width, height, color_num = 1):
    '''
    Рисует высотное здание с выбором цвета.
    -------------------------------------
    x - горизонтальная координата нижнего левого угла здания
    y - вертикальная координата нижнего левого угла здания относительно
    горизонта
    width - ширина здания
    height - высота здания
    color_num - номер цвета city для рисования
    '''
    pgd.rect(screen, CITY_COLOR[color_num], (x, Horizon + y - height, width, height))
    
def cloud (x, y, width, height, impidity):
    '''
    Рисует облако с заданной прозрачностью.
    -------------------------------------
    x - горизонтальная координата нижнего левого угла прямоугольника, 
    в который вписано облако;
    y - вертикальная координата нижнего левого угла прямоугольника, 
    в который вписано облако, относительно горизонта;
    width - ширина облака (большая ось);
    height - высота облака (малая ось);
    impidity - параметр прозрачности (облако имеет чёрную заливку с некоторой 
    прозрачностью).
    '''
    surf = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    surf = surf.convert_alpha()
    surf.set_alpha(impidity)
    
    pgd.ellipse(surf, (0, 0, 0, impidity), (0, 0, width, height))
     
    screen.blit(surf, (x, Horizon + y - height))
    
def car (x, y, scale = 1):
    '''
    Рисует машинку с заданным масштабом.
    -------------------------------------
    x - горизонтальная координата нижнего левого угла прямоугольника,
    изображающего тело машинки;
    y - вертикальная координата нижнего левого угла прямоугольника, 
    изображающего тело машинки, относительно горизонта;
    scale - масштаб, множитель размера по-умолчанию.
    '''
    '''Труба'''
    if scale > 0:
        pgd.ellipse(screen, CAR_COLOR['WHEEL'], (int(x - 15*scale), int(Horizon + y - 20*scale), int(20*scale), int(8*scale)))
    else:
        pgd.ellipse(screen, CAR_COLOR['WHEEL'], (int(x - 5*abs(scale)), int(Horizon + y - 20*abs(scale)), int(20*abs(scale)), int(8*abs(scale))))
    '''Кузов'''
    pgd.rect(screen, CAR_COLOR['BODY'], (int(x), int(Horizon + y - 40*abs(scale)), int(150*scale), int(40*abs(scale))))
    pgd.rect(screen, CAR_COLOR['BODY'], (int(x + 20*scale), int(Horizon + y - 70*abs(scale)), int(80*scale), int(30*abs(scale))))
    '''Колёса'''
    pgd.circle(screen, CAR_COLOR['WHEEL'], (int(x + 30*scale), int(Horizon + y)), int(20*abs(scale)))
    pgd.circle(screen, CAR_COLOR['WHEEL'], (int(x + 110*scale), int(Horizon + y)), int(20*abs(scale)))
    '''Окна'''
    pgd.rect(screen, CAR_COLOR['WINDOW'], (int(x + 25*scale), int(Horizon + y - 65*abs(scale)), int(38*scale), int(20*abs(scale))))
    pgd.rect(screen, CAR_COLOR['WINDOW'], (int(x + 70*scale), int(Horizon + y - 65*abs(scale)), int(26*scale), int(20*abs(scale))))
    
def shadow (x, width, height, impidity):
    '''
    Рисует тень далёкого высотного здания, которая начинается на горизонте и
    имеет заданную прозрачность
    -------------------------------------
    x - горизонтальная координата нижнего левого угла тени вдоль горизонта
    width - ширина тени
    height - высота тени
    impidity - прозрачность тени
    '''
    surf = pygame.Surface((width, height))
    surf.fill(BLACK_COLOR)
    surf.set_alpha(impidity)
    screen.blit(surf, (x, Horizon - height))


def blick (x, y, grade = 0.4, radius = 1000):
    '''
    Создаёт белый блик с гиперболическим градиентом заданной степени
    -------------------------------------
    x - горизонтальная координата блика
    y - вертикальная координата блика относительно горизонта
    grade - степень гиперболы, которая задаёт градиент
    radius - радиус блика 
    '''
    R = np.arange (start = 2, stop = radius, step = 1)
    for  r_i in R:
        impidity = 255/(r_i)**grade
        blickCycle (x - r_i, y - r_i, r_i, impidity)

def blickCycle (x, y, R, impidity):
    '''
    Рисует окружность заданной прозрачности, толщины 1
    -------------------------------------
    x - горизонтальная координата центра окружности
    y - вертикальная координата центра окружности относительно горизонта
    R - радиус окружности
    impidity - прозрачность окружности
    '''
    surf = pygame.Surface((2*R, 2*R), pygame.SRCALPHA, 32)
    surf = surf.convert_alpha()
    surf.set_alpha(impidity)
    
    pgd.circle(surf, (255, 255, 255, impidity), (R, R), R, 2)
     
    screen.blit(surf, (x, Horizon + y))






