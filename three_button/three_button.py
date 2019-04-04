import pyglet
import math
import random
from pyglet.window import key

window = pyglet.window.Window(caption="Three-Button Game")

class GameObject:
    '''Keeps all game info together, so I won't have to make all kinds of
    variables global, like in first version, which turned crazy on me.'''
    def __init__(self):
        #possible mode values: resting, playing, splash, instructions, gameover
        self.mode = "splash"
        self.score = 0
        self.lives = 3
        self.round_time = 1.00  # the time, in seconds, the player has to respond to one round
        self.rest_time = 0.50   # the time, in seconds, between one round and the next
        self.rect = ()          # holds the rectangle currently being displayed
        self.num_rounds = 0     # i don't think this ever got used

        #I create several text labels for use later in the game.
        #Graphics batches will hold all the labels for each screen.

        #Splash screen batch and labels
        self.splash_batch = pyglet.graphics.Batch()

        self.title_label = pyglet.text.Label(text="Three-Button Game",
                                        font_name='Arial',
                                        font_size=36,
                                        anchor_x='center',
                                        anchor_y='bottom',
                                        x=window.width/2,
                                        y=window.height/2,
                                        color=(255, 255, 0, 255),
                                        batch=self.splash_batch)

        self.sub_title_label = pyglet.text.Label("'I' for instructions   Any other key to play",
                                            font_name='Arial',
                                            font_size=18,
                                            anchor_x='center',
                                            anchor_y='top',
                                            x=window.width/2,
                                            y=window.height/2 - 20,
                                            color=(255, 0, 0, 255),
                                            batch=self.splash_batch
                                            )

        #Instruction screen batch and labels.
        #I use a for loop to create labels for the the multiline instructions.
        self.instructions_text = ["Press 'z' when the left side of the screen lights up",
        "Press 'x' when the center of the screen lights up",
        "Press 'c' when the right side of the screen lights up",
        "If you are too slow or press the wrong key, you lose a life",
        "Game Over when you run out of lives",
        "Press any key to start"]

        inc = -2
        self.instructions_batch = pyglet.graphics.Batch()

        for line in self.instructions_text:
            label = pyglet.text.Label(text=line,
                                      font_name="Arial",
                                      font_size=18,
                                      anchor_x="center",
                                      anchor_y="center",
                                      x=window.width/2,
                                      y=window.height/2-(inc*25),
                                      color=(255, 0, 0, 255),
                                      batch=self.instructions_batch)
            inc += 1


        #Game over batch and labels
        self.game_over_batch = pyglet.graphics.Batch()

        self.game_over_label = pyglet.text.Label("GAME OVER",
                          font_name='Arial',
                          font_size=36,
                          anchor_x='center',
                          anchor_y='bottom',
                          x=window.width/2,
                          y=window.height/2,
                          color=(255, 0, 0, 255),
                          batch=self.game_over_batch
                          )
        self.sub_game_over_label = pyglet.text.Label("ESC to quit    ENTER to play again",
                          font_name='Arial',
                          font_size=18,
                          anchor_x='center',
                          anchor_y='top',
                          x=window.width/2,
                          y=window.height/2,
                          color=(255, 0, 0, 255),
                          batch=self.game_over_batch
                          )

        #Score and lives batch and labels
        self.stats_batch = pyglet.graphics.Batch()

        self.score_label = pyglet.text.Label(text='Score: {}'.format(self.score),
                                        font_name='Arial',
                                        font_size=18,
                                        anchor_x='left',
                                        anchor_y='top',
                                        x=0,
                                        y=window.height,
                                        color=(0, 255, 0, 255),
                                        batch=self.stats_batch
                                        )

        self.lives_label = pyglet.text.Label(text='Lives: {}'.format(self.lives),
                                        font_name='Arial',
                                        font_size=18,
                                        anchor_x='right',
                                        anchor_y='top',
                                        x=window.width,
                                        y=window.height,
                                        color=(255, 0, 0, 255),
                                        batch=self.stats_batch
                                        )

        #These lines define coords for eight points that will be used to draw the three rects on screen.
        #They will adapt to the size of the screen.
        self.TOP = window.height
        self.BOTTOM = 0
        self.FIRST = 0
        self.SECOND = int(window.width / 3)
        self.THIRD = self.SECOND * 2
        self.FOURTH = window.width

        #Here the three rects are defined
        self.LEFT =  ('v2i',
                (self.FIRST, self.TOP,
                 self.SECOND, self.TOP,
                 self.FIRST, self.BOTTOM,
                 self.SECOND, self.BOTTOM
                ))
        self.MIDDLE =    ('v2i',
                    (self.SECOND, self.TOP,
                     self.THIRD, self.TOP,
                     self.SECOND, self.BOTTOM,
                     self.THIRD, self.BOTTOM
                    ))
        self.RIGHT = ('v2i',
                (self.THIRD, self.TOP,
                 self.FOURTH, self.TOP,
                 self.THIRD, self.BOTTOM,
                 self.FOURTH, self.BOTTOM
                ))
        #RECTANGLES holds the three rects, ready to be selected at random.
        self.RECTANGLES = (self.LEFT, self.MIDDLE, self.RIGHT)

    def score_point(self):
        """score_points is called when the player gets a point."""
        pyglet.clock.unschedule(self.too_long)
        self.score = self.score + 1
        self.score_label.text = 'Score: {}'.format(self.score)
        self.take_rest()

    def penalty(self, dt):
        """penalty is called when a life is lost, either because the player
        was too slow, or pressed the wrong key.
        It also slows the game down a little, for the player's benefit."""
        self.lives = self.lives - 1
        self.round_time *= 1.1
        self.rest_time *= 1.1
        self.lives_label.text = 'Lives: {}'.format(self.lives)
        if self.lives < 1:
            self.end_game()

    def start_game(self):
        """start_game is called when the player restarts the game, to reinitialize
        all the game variables."""
        self.mode = "splash"
        self.score = 0
        self.lives = 3
        self.round_time = 1.00
        self.rest_time = 0.50
        self.rect = ()
        self.num_rounds = 0
        self.score_label.text = 'Score: {}'.format(self.score)
        self.lives_label.text = 'Lives: {}'.format(self.lives)

    def end_game(self):
        """end_game is called when the player has no more lives left."""
        pyglet.clock.unschedule(self.too_long)
        pyglet.clock.unschedule(self.new_round)
        self.mode = "gameover"

    def too_long(self, dt):
        """too_long is called when the player is too slow in responding to the game.
        It calls penalty to finish the task of punishing the player."""
        self.take_rest()
        self.penalty(0)

    def wrong_button(self):
        """wrong_button is called when the player presses the wrong key while playing.
        It calls penalty to finish the task of punishing the player."""
        pyglet.clock.unschedule(self.too_long)
        self.take_rest()
        self.penalty(0)

    def take_rest(self):
        """take_rest is called between each round, regardless of wether the player wins or
        loses the round."""
        self.mode = "resting"
        pyglet.clock.schedule_once(self.new_round, self.rest_time)

    def new_round(self, dt):
        """new_round is called when take_rest is done to pick a new rectangle to display,
        and set the timer for the player to respond. It also  shrinks the round length and
        rest length to make the game go progressively faster over time."""
        self.mode = "playing"
        r = math.floor(random.random() * 3)
        self.rect = self.RECTANGLES[r]
        pyglet.clock.schedule_once(self.too_long, self.round_time)
        self.round_time *= 0.99
        self.rest_time *= 0.99
        #print("round_time: {} -- rest_time: {}".format(self.round_time, self.rest_time))


@window.event
def on_draw():
    """on_draw clears the screen and draws the new frame based on what mode the game is in."""
    window.clear()
    if the_game.mode == "splash":
        the_game.splash_batch.draw()
    elif the_game.mode == "instructions":
        #the_game.instructions_label.draw()
        the_game.instructions_batch.draw()
    elif the_game.mode == "gameover":
        the_game.game_over_batch.draw()
    elif the_game.mode == "resting":
        pass
    elif the_game.mode == "playing":
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 1, 2, 3], the_game.rect)

    the_game.stats_batch.draw()



@window.event
def on_key_press(symbol, modifiers):
    """on_key_press responds to user input based on what mode the game is currently in."""
    global the_game
    if the_game.mode == "splash":
        if symbol == key.I:
            the_game.mode = "instructions"
        else:
            the_game.take_rest()
    elif the_game.mode == "instructions":
        the_game.take_rest()
    elif the_game.mode == "gameover":
        if symbol == key.ENTER:
            the_game.start_game()
    elif the_game.mode == "resting":
        pass
    elif the_game.mode == "playing":
        if symbol == key.Z and the_game.rect == the_game.LEFT:
            the_game.score_point()
        elif symbol == key.X and the_game.rect == the_game.MIDDLE:
            the_game.score_point()
        elif symbol == key.C and the_game.rect == the_game.RIGHT:
            the_game.score_point()
        else:
            the_game.wrong_button()

#Initialize the game object and start the program!
the_game = GameObject()
pyglet.app.run()
