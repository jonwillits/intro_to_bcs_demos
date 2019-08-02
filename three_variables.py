import tkinter as tk
from turtle import RawTurtle, TurtleScreen
import numpy as np
import math


def create_canvas():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()

    wn = TurtleScreen(canvas)

    button_frame = tk.Frame(root)
    button_frame.pack()

    return wn, button_frame


def draw_axes(wn):
    # draw the axes
    x = RawTurtle(wn)
    x.hideturtle()
    y = RawTurtle(wn)
    y.hideturtle()
    z = RawTurtle(wn)
    z.hideturtle()

    z_axis = np.linspace(0, 300, 2)
    x_axis = np.sin(z_axis)
    y_axis = np.cos(z_axis)

    for i in range(len(z_axis)):
        print(z_axis[i], x_axis[i], y_axis[i])

    x2d = x_axis - z_axis * math.cos(math.radians(45))
    y2d = y_axis - z_axis * math.sin(math.radians(45))
    print()
    for i in range(len(z_axis)):
        print(z_axis[i], x2d[i], y2d[i])

    for i in range(len(x_axis)):
        x.goto(z_axis[i], 0)
        print(x.position())
        y.goto(0, z_axis[i])
        print(y.position())
    x.write("x", font = ("Arial", 30, "normal"))
    y.write("y", font = ("Arial", 30, "normal"))
    for i in range(len(x2d)):
        z.goto(x2d[i], y2d[i])


    z.penup()
    z.goto(-210, -200)
    z.pendown()
    z.write("z", font = ("Arial", 30, "normal"))


def convert_projection(wn):
    zline = np.linspace(0, 15, 1000)
    xline = np.sin(zline)
    yline = np.cos(zline)

    global x2D
    x2D = xline - zline * math.cos(math.radians(45))
    global y2D
    y2D = yline - zline * math.sin(math.radians(45))

    global c
    c = RawTurtle(wn)
    c.hideturtle()
    c.penup()
    c.goto(x2D[0] * 20, y2D[0] * 20)
    c.pendown()


def draw_curve():
    # draw the curve
    global running
    running = True

    if c.xcor() == x2D[0] * 20 and c.ycor() == y2D[0] * 20:
        for i in range(len(x2D)):
            c.goto(x2D[i] * 20, y2D[i] * 20)
            print(c.position())
            if c.xcor() == x2D[len(x2D) - 1] and c.ycor() == y2D[len(y2D) - 1]:
                break
            if running == False:
                break
    else:
        for i in range(len(x2D)):
            if c.xcor() == x2D[i] * 20:
                index = i
                while index < len(x2D) - 1:
                    if running == False:
                        break
                    c.goto(x2D[index + 1] * 20, y2D[index + 1] * 20)
                    index += 1


def stop_drawing():
    global running
    running = False


def main():
    wn, button_frame = create_canvas()
    draw_axes(wn)
    # convert_projection(wn)
    # tk.Button(button_frame, text="run", fg="black", command=draw_curve).pack(side=tk.LEFT)
    # tk.Button(button_frame, text="stop", fg="black", command=stop_drawing).pack(side=tk.RIGHT)
    wn.mainloop()

main()


