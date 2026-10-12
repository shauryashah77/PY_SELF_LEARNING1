import math
import turtle
import easygui

SHAPES = ["Square", "Equilateral Triangle", "Concentric Circles", "Custom Star"]
DEFAULT_COLOR = "blue"


def get_shape_choice():
    return easygui.buttonbox(
        "Choose a shape to draw:",
        title="Geometric Art Studio",
        choices=SHAPES,
    )


def get_dimension():
    return easygui.integerbox(
        "Enter the size / radius (50 to 250):",
        title="Dimension",
        default=100,
        lowerbound=50,
        upperbound=250,
    )


def get_fill_color():
    color = easygui.enterbox(
        "Enter a fill color (e.g. blue, red, teal):",
        title="Fill Color",
        default=DEFAULT_COLOR,
    )
    if color is None:
        return None
    color = color.strip().lower()
    return color if color else DEFAULT_COLOR


def is_valid_color(color):
    probe = turtle.Turtle()
    probe.hideturtle()
    try:
        probe.color(color)
        return True
    except Exception:
        return False
    finally:
        probe.clear()


def setup_canvas():
    screen = turtle.Screen()
    screen.title("Geometric Art Studio")
    screen.setup(width=700, height=700)
    screen.bgcolor("white")
    pen = turtle.Turtle()
    pen.speed(3)
    pen.pensize(2)
    return screen, pen


def move_to(pen, x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()


def draw_polygon(pen, points, color):
    move_to(pen, *points[0])
    pen.color("black", color)
    pen.begin_fill()
    for x, y in points[1:]:
        pen.goto(x, y)
    pen.goto(*points[0])
    pen.end_fill()


def draw_square(pen, side, color):
    half = side / 2
    points = [(-half, -half), (half, -half), (half, half), (-half, half)]
    draw_polygon(pen, points, color)


def draw_triangle(pen, side, color):
    height = side * math.sqrt(3) / 2
    points = [
        (-side / 2, -height / 3),
        (side / 2, -height / 3),
        (0, 2 * height / 3),
    ]
    draw_polygon(pen, points, color)


def draw_concentric_circles(pen, radius, color):
    rings = 4
    step = radius / rings
    for i in range(rings):
        current = radius - i * step
        fill = color if i % 2 == 0 else "white"
        move_to(pen, 0, -current)
        pen.color("black", fill)
        pen.begin_fill()
        pen.circle(current)
        pen.end_fill()


def draw_star(pen, radius, color):
    outer = [
        (
            radius * math.cos(math.radians(90 + i * 72)),
            radius * math.sin(math.radians(90 + i * 72)),
        )
        for i in range(5)
    ]
    points = [outer[(i * 2) % 5] for i in range(5)]
    draw_polygon(pen, points, color)


def draw_shape(pen, shape, size, color):
    drawers = {
        "Square": draw_square,
        "Equilateral Triangle": draw_triangle,
        "Concentric Circles": draw_concentric_circles,
        "Custom Star": draw_star,
    }
    drawers[shape](pen, size, color)
    pen.hideturtle()


def collect_inputs():
    shape = get_shape_choice()
    if shape is None:
        return None
    size = get_dimension()
    if size is None:
        return None
    color = get_fill_color()
    if color is None:
        return None
    if not is_valid_color(color):
        easygui.msgbox(
            "Unknown color. Using " + DEFAULT_COLOR + " instead.",
            title="Color Notice",
        )
        color = DEFAULT_COLOR
    return shape, size, color


def main():
    inputs = collect_inputs()
    if inputs is None:
        return
    shape, size, color = inputs
    screen, pen = setup_canvas()
    try:
        draw_shape(pen, shape, size, color)
        easygui.msgbox(
            "Your " + shape + " has been drawn successfully!",
            title="Drawing Complete",
        )
    finally:
        try:
            turtle.bye()
        except Exception:
            pass


if __name__ == "__main__":
    main()
