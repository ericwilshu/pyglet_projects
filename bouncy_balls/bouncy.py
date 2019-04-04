import pyglet
import math
import random


class Ball(pyglet.sprite.Sprite):
    """
    The ball class inherits from pyglet's Sprite class, and adds to it extra
    properties and methods to set a single circle bouncing around the screen.
    These balls will bounce off the borders of the window.
    """
    def __init__(self, image, lx, ly, dx, dy, size, hue, what_batch):
        """
        __init__ need the image, xy coords, and batch to send up to the Sprite
        constructor. Also, it used dx and dy to determine its motion, scale to
        determine its size relative to the original sprite graphic, and its
        color(the original sprite images should be white on transparent bg's).
        """
        super(Ball, self).__init__(img=image, x=lx, y=ly, batch=what_batch)
        self.dx = dx
        self.dy = dy
        self.scale = size
        self.color = hue

    def move(self, dt):
        """
        Moves ball according to pyglet's main loop's dt variable and ball's own
        dx and dy properties. Then checks for collisions with window borders.
        """
        self.x += self.dx*dt
        self.y += self.dy*dt
        self.check_bounds()

    def check_bounds(self):
        """
        Checks if the ball has collided with the window border. Collision with
        top or bottom results in reversing dy. With left or right reverses dx.
        """
        if self.x + self.width / 2 > window.width:
            self.x = window.width - self.width / 2
            self.dx *= -1
        elif self.x - self.width / 2 < 0:
            self.x = self.width / 2
            self.dx *= -1

        if self.y + self.height / 2 > window.height:
            self.y = window.height - self.height / 2
            self.dy *= -1
        elif self.y - self.height / 2 < 0:
            self.y = self.height / 2
            self.dy *= -1

if __name__ == "__main__":
    window = pyglet.window.Window(width=1000, height=1000, caption="Bouncy!")
    #window = pyglet.window.Window(fullscreen=True)
    fps_display = pyglet.window.FPSDisplay(window)


    # setting up the resource path so we can easily import the sprite graphic and bg
    pyglet.resource.path = ['./img']
    pyglet.resource.reindex()

    bg_image = pyglet.resource.image('bg.gif')

    ball_image = pyglet.resource.image('ball2.gif')
    ball_image.anchor_x = ball_image.width/2
    ball_image.anchor_y = ball_image.height/2


    @window.event
    def on_draw():
        """
        On draw runs every time through the main loop supplied by pyglet.
        """
        window.clear()
        bg_sprite.draw()
        main_batch.draw()
        fps_display.draw()

    def update(dt):
        """
        Updates all the balls in ball list, in preparation for drawing them.
        """
        for ball in ball_list:
            ball.move(dt)

    def get_random_color(alpha=False):
        """
        Utility function for randomizing each ball's and bg's color.
        """
        if alpha:
            return (random.random(), random.random(), random.random(), 1.0)
        else:
            return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


    # set the bg image to a random color and the size of the window.
    bg_sprite = pyglet.sprite.Sprite(img=bg_image, x=0, y=0)
    bg_sprite.scale_x = window.width / bg_sprite.width
    bg_sprite.scale_y = window.height / bg_sprite.height
    bg_sprite.color = get_random_color()

    """
    Create a graphics batch and list for however many balls we want.
    main_batch is used to draw the balls, ball_list is used to loop through
    all the balls and update them.
    """
    main_batch = pyglet.graphics.Batch()
    ball_list = []
    for i in range(100):
        the_ball = Ball(ball_image,
                        random.randint(0, window.width),
                        random.randint(0, window.height),
                        random.randint(-600, 600),
                        random.randint(-600, 600),
                        random.random() * 1.0,
                        #0.25,
                        get_random_color(),
                        #(0, 0, 0),
                        main_batch
                        )
        ball_list.append(the_ball)


    # Set the clock and run the app!
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()
