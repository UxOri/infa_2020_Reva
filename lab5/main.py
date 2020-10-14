import core
import dialog

'''Спрашиваем имя'''
app = dialog.SampleApp()
app.mainloop()
NAME = app.text_out()
POINTS = 0

core.pygame.display.update()
clock = core.pygame.time.Clock()
finished = False

kit = core.Balls(core.screen, core.init_balls(10, 50, kenny_chance = 20))

'''Главный исполняющий цикл'''
while not finished:
    clock.tick(core.FPS)
    for event in core.pygame.event.get():
        if event.type == core.pygame.QUIT:
            print(POINTS)
            finished = True
        elif event.type == core.pygame.MOUSEBUTTONDOWN:
            dp = core.click(event, kit)
            POINTS += dp
    kit.move(1/core.FPS)
    kit.show()
    core.pygame.display.update()
    core.screen.fill(core.COLOR['Black'])

core.pygame.quit()

'''Записываем результат в таблицу рекордов'''
place = core.insert(NAME, POINTS)

'''Сообщаем игроку о его результатах и месту в рейтинге игроков'''
root = core.Tk()
root.withdraw()                
core.showinfo(title = "Game over", message = "Ваши результаты занесены в таблицу лидеров \n Ваше место: {}".format(place))
root.destroy()