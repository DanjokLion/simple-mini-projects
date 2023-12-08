from tkinter import *
import random

tk = Tk()
c = Canvas(tk, width=640, height=640, bg='white')
c.pack()

asteroid_image = PhotoImage(file='asteroid.gif')
player_image = PhotoImage(file='player.gif')
sky_image = PhotoImage(file='sky.gif')

c.create_image(0,0, image=sky_image, anchor=NW)

vx, vy = 10, 15
xSpeed, ySpeed = [], []
asteroids = []

for x in range(1,11):
    x = random.randint(20, 610)
    y = random.randint(20, 610)

    asteroid = c.create_image(x, y, image=asteroid_image, anchor=NW)
    vx = random.randint(-15, 15)
    vy = random.randint(-15, 15)
    asteroids.append(asteroid)

    xSpeed.append(vx)
    ySpeed.append(vy)

player = c.create_image(300,300, image=player_image, acnhor=NW)

def moveBall():
    for i in range(1,11):

        asteroid = asteroids[i]
        vx = xSpeed[i]
        vy = ySpeed[i]

        x1, y1 = c.coords(asteroid)
        x2 = x1 + 40
        y2 = y1 + 40

        if x1 <= 0 or x2 >= 640:
            vx *= -1
        if y1 <= 0 or y2 >= 640:
            vy *= -1

        xSpeed[i] = vx
        ySpeed[i] = vy

        c.move(asteroid, vx, vy)

    c.after(50, moveBall)

c.after(50, moveBall)


def movePlayer(key):
    match key:
        case 'a':
            c.move(player, -20, 0)
        case 'd':
            c.move(player, 20, 0)
        case 'w':
            c.move(player, 0, -20)
        case 's':
            c.move(player, 0, 20)


tk.bing('<KeyPress>', movePlayer)

mainloop()