import turtle


def draw_petal():
    """
    this function uses the turtle module
    to draw one flower petal
    """
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)


def draw_flower():
    """
    this functions uses the draw_petal function 
    and draws an entire upside down flower
    """
    turtle.left(45)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(135)
    turtle.forward(150)


def draw_flower_advanced():
    """
    this functions uses the draw_flower function 
    it draws an entire upside down flower
    and follows by moving the turtle we created
    in the direction of it's initial angle 
    along it's initial y coordinate, by 150
    """
    draw_flower()
    turtle.right(90)
    turtle.up()
    turtle.forward(150)
    turtle.right(90)
    turtle.forward(150)
    turtle.left(90)
    turtle.down()


def draw_flower_bed():
    """
    this functions uses the draw_flower_advanced function 
    it moves the turtle we created to a new position and angle
    and continues drawing 3 separate flowers
    """
    turtle.up()
    turtle.forward(200)
    turtle.left(180)
    turtle.down()
    draw_flower_advanced()
    draw_flower_advanced()
    draw_flower_advanced()


draw_flower_bed()
turtle.done()
