import pygame
import pygame.draw as pgd

'''Размер окна и горизонт'''
X = 600
Y = 900
Horizon = 450
screen = pygame.display.set_mode((X, Y))

'''Цвета'''
SKY_COLOR        = (110, 110, 110)
GROUND_COLOR     = (110, 133, 129)
CAR_BODY_COLOR   = (117, 199, 214)
CAR_WINDOW_COLOR = (188, 212, 212)
CAR_WHEELS_COLOR = ( 49,  79,  84)
CITY_1_COLOR     = (183, 200, 196, 0)
CITY_2_COLOR     = (200, 213, 210)
CITY_3_COLOR     = (147, 172, 167)
CITY_4_COLOR     = (175, 192, 194)
CITY_5_COLOR     = (120, 152, 145)

def background ():
    '''
    Рисует небо и землю, разделяя их на горизонте.
    -------------------------------------
    '''
    pgd.rect(screen, SKY_COLOR, (0, 0, X, Y))
    pgd.rect(screen, GROUND_COLOR, (0, Horizon, X, Y/2))
    
def cityColor (num):
    '''
    Возвращает цвет city по номеру
    -------------------------------------
    num - номер цвета city
    '''
    if   num == 1:
        return CITY_1_COLOR 
    elif num == 2:
        return CITY_2_COLOR 
    elif num == 3:
        return CITY_3_COLOR 
    elif num == 4:
        return CITY_4_COLOR 
    elif num == 5:
        return CITY_5_COLOR 
    
def building (x, y, width, height, color_num = 1):
    '''
    Рисует высотное здание с выбором цвета.
    -------------------------------------
    x - горизонтальная координата нижнего правого края здания
    y - вертикальная координата нижнего правого края здания относительно
    горизонта
    width - ширина здания
    height - высота здания
    color_num - номер цвета city для рисования
    '''
    pgd.rect(screen, cityColor(color_num), (x, Horizon + y - height, width, height))
    
def cloud (x, y, width, height, impidity):
    '''
    Рисует облако с заданной прозрачностью
    -
    '''
    surf = pygame.Surface((width, height))
    surf.fill((SKY_COLOR))
    surf.set_alpha(impidity)
    
    pgd.ellipse(surf, (0, 0, 0), (0, 0, width, height))
     
    screen.blit(surf, (x, Horizon + y - height))
    
def car (x, y, scale):
    ''''''
    #pgd.rect(screen, )
    
    
    