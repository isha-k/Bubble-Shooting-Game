import turtle
import math
import random
import winsound


class Game():
    def __init__(self) -> None:
        self.base = turtle.Turtle()
        self.shooter = turtle.Turtle()
        self.balloon = turtle.Turtle()
        self.bullet = turtle.Turtle()
        self.bullet_state = 'ready'
        self.game_over = 'No'
        self.missed_shots = 0
        self.shots = 0
        self.dy = 10  # Set balloon speed

        # Initialise cannon base
        self.base.speed(0)
        self.base.shape("square")
        self.base.color("white")
        self.base.shapesize(stretch_wid=3, stretch_len=4.5)
        self.base.penup()
        self.base.goto(340, 0)

        # Initialise cannon shooter
        self.shooter.speed(0)
        self.shooter.shape("square")
        self.shooter.color("white")
        self.shooter.penup()
        self.shooter.shapesize(stretch_len=2)
        self.shooter.goto(280, 0)

        # Initialise balloon
        self.balloon.speed(0)
        self.balloon.shape("circle")
        self.balloon.color("purple", "turquoise")
        self.balloon.shapesize(stretch_wid=2, stretch_len=2, outline=3)
        self.balloon.penup()
        self.balloon.setposition(-340, 0)

        # Initialise bullet
        self.bullet.speed(0)
        self.bullet.shape("square")
        self.bullet.color("gray")
        self.bullet.penup()
        self.bullet.hideturtle()

    def canon_up(self) -> None:
        """ Function moves cannon up when player presses 'Up' key
        :return: None

        """
        if not self.base.ycor() > 240:  # Upper border check
            y = self.base.ycor()
            y += 20
            self.base.sety(y)
            self.shooter.sety(y)

    def canon_down(self) -> None:
        """ Function moves cannon down when player presses the 'Down' key
        :return: None

        """
        if not self.base.ycor() < -240:  # Lower border check
            y = self.base.ycor()
            y -= 20
            self.base.sety(y)
            self.shooter.sety(y)

    def shoot(self) -> None:
        """ Function fires bullet when player presses 'space' key
        :return: None

        """
        if self.bullet_state == 'ready':  # If bullet ready, change state to 'fire'
            self.bullet_state = 'fire'
            self.bullet.setposition(self.shooter.xcor(),
                                    self.shooter.ycor())  # Set bullet position at shooter's co-ords
            self.bullet.showturtle()

        if self.bullet_state == 'fire':  # If bullet's state is 'fire', shoot the bullet
            winsound.PlaySound("space.wav", winsound.SND_ASYNC)  # Add sound to accompany bullet shot
            while self.bullet_state == 'fire':
                self.bullet.setx(self.bullet.xcor() - 15)  # Bullet speed should be 1.5*balloon speed (10 * 1.5) = 15
                self.balloon.sety(
                    self.balloon.ycor() + 1.3 * self.dy)  # Ensures that balloon continues moving with bullet

                # Check borders
                if self.balloon.ycor() > 290:
                    self.balloon.sety(290)
                    self.dy *= -1
                elif self.balloon.ycor() < -290:
                    self.balloon.sety(-290)
                    self.dy *= -1

                # Balloon randomly changes directions
                if abs(random.randint(-300, 300)) == abs(random.randint(-300, 300)):
                    self.dy *= -1

                # Check for bullet and balloon collision
                if self.is_collision():
                    self.bullet_state = 'ready'
                    self.game_over = 'Yes'  # Set game_over state to 'Yes' if collision successful
                    self.missed_shots = self.shots  # Save number of missed shots

                # Check if bullet is out of the game
                if self.bullet.xcor() < -400:
                    self.bullet_state = 'ready'  # If bullet out of game, cannon is ready to shoot again
                    self.bullet.hideturtle()
                    self.shots += 1  # If bullet out of game then no bullet-balloon collision, increment misses

    def is_collision(self) -> bool:
        """ Function checks for a collision between balloon and bullet
        :return: boolean -> True if collision, False if no collision

        """
        distance = math.sqrt(
            math.pow(self.bullet.xcor() - self.balloon.xcor(), 2) + math.pow(self.bullet.ycor() - self.balloon.ycor(),
                                                                             2))
        if distance < 25:
            return True
        else:
            return False


if __name__ == '__main__':

    # Set up screen
    wn = turtle.Screen()
    wn.title("Balloon Shooting Challenge")  # Set title
    wn.bgcolor("white")  # Set background colour
    wn.bgpic("cave.gif")  # Set background picture
    wn.setup(width=800, height=600)  # Set dimensions

    game = Game()  # Instantiate Game Class

    # Keyboard bindings
    wn.listen()
    wn.onkey(game.canon_up, 'Up')
    wn.onkey(game.canon_down, 'Down')
    wn.onkey(game.shoot, 'space')

    # Main loop
    running = True
    while running:
        wn.update()  # Ensures screen remains open

        # Move balloon
        game.balloon.sety(game.balloon.ycor() + game.dy)

        # Border check
        if game.balloon.ycor() > 290:
            game.balloon.sety(290)
            game.dy *= -1
        elif game.balloon.ycor() < -290:
            game.balloon.sety(-290)
            game.dy *= -1

        # Randomly move balloon up and down
        if abs(random.randint(-300, 300)) == abs(random.randint(-300, 300)):
            game.dy *= -1

        # If balloon shot down, game is over. Display number of missed shots
        if game.game_over == 'Yes':
            misses = game.shots
            wn.clear()
            wn.bgpic("game.gif")
            t = turtle.Turtle()
            t.hideturtle()
            style1 = ('Comic Sans', 30, 'bold')
            t.color('black')
            t.penup()
            t.goto(0, -150)
            t.pendown()
            string = 'Number of missed shots: ' + str(misses)
            t.write(string, font=style1, align='center')

            turtle.done()



    wn.bye()
