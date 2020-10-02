from Pic import*

pygame.init()

FPS = 30

background()
cloud(400, -220, 300, 100, 50)
shadow(400, 100, 1000, 100)
building(100, 20, 200, 500)
blick(200, 100)

car (200, 200, scale = 1.2)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()