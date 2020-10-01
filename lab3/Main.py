from Pic import*

pygame.init()

FPS = 30

background()
building(100, 20, 200, 500)
cloud(400, -220, 300, 100, 50)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()