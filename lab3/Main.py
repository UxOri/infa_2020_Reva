from Pic import*

pygame.init()

FPS = 30

background()
cloud(400, -220, 300, 100, 50)
cloud(200, -200, 400,  80, 80)
cloud(100, -300, 200, 100, 40)
shadow(  0, 100, 300, 200)
shadow( 50, 200, 350, 150)
shadow(  0, 150, 250, 220)
shadow(100, 120, 300, 200)
blick(0, -450, grade = 0.35)

building(300,   0, 200, 430, color_num = 0)
building(  0,   0, 300, 200, color_num = 3)
building(400,   0, 390, 300, color_num = 4)
building(150,  50, 400, 300, color_num = 2)
building(450, 100, 130, 200, color_num = 1)

car(100, 200)
car(400, 200)
car(100, 100, scale = -0.4)
car(300, 100, scale = -0.4)
car(500, 100, scale = -0.4)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()