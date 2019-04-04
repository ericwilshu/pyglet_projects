import pyglet
from math import floor
from random import randint, random


class PointBurst(pyglet.text.Label):
    '''
    The PointBurst class displays a text label which floats upward,
    grows in size, and fades out. It is meant to be used to indicate
    points scored in a video game.
    '''
    def __init__(self,
                 points,        # the text to display
                 font,
                 start_size,    # the label starts with this font size
                 x_loc,
                 y_loc,
                 color,
                 life,          # this is how long (in seconds) the label takes to fade out
                 distance,      # this is how far (in pixels) the label will float upwards
                 end_size,      # the label ends with this font size
                 what_batch):
        super(PointBurst, self).__init__(text=str(points),
                                         font_name=font,
                                         font_size=start_size,
                                         x=x_loc,
                                         y=y_loc,
                                         anchor_x='center',
                                         anchor_y='bottom',
                                         color=color,
                                         batch=what_batch)
        self.dead = False
        self.fsize = self.font_size * 1.0   # font-size stored as a float
        #self.xf = self.x * 1.0              # x coord stored as a float
        self.yf = self.y * 1.0              # y coord stored as a float
        self.life = life
        self.distance = distance
        self.pix_per_sec = self.distance / self.life
        self.visibility = self.color[3] * 1.0   # visibility stored as a float
        self.vis_per_sec = self.visibility / self.life
        self.end_size = end_size
        self.grow_per_second = (self.end_size - start_size) / self.life


    def update(self, dt):
        '''
        This function should be called every frame to update the point burst.
        Most of these values need to be figured as floats, and then converted to
        integers to update the display. Otherwise the change in each frame might
        remain too small to ever take effect.
        '''
        if not self.dead:
            self.fsize = self.fsize + self.grow_per_second * dt
            self.font_size = floor(self.fsize)
            self.yf = self.yf + self.pix_per_sec * dt
            self.y = floor(self.yf)
            self.visibility = self.visibility - self.vis_per_sec * dt
            self.color = (self.color[0], self.color[1], self.color[2], floor(self.visibility))
            if self.visibility < 1.0:
                self.visibility = 0.0
                self.dead = True
                self.batch = None



class PointBurstGroup():
    '''
    A convenient class to hold all the point bursts being used at any given time.
    '''
    def __init__(self):
        #self.window = window
        self.pb_batch = pyglet.graphics.Batch() # tells the point bursts which graphics batch to render with
        self.pb_list = []   # list to hold all the point bursts in this group
        self.dead_pbs = []  # list to hold all the point bursts that have faded out


    def add_pb( self,
                points=100,
                font='Arial',
                start_size=30,
                x_loc=0,
                y_loc=0,
                color=(255, 255, 255, 255),
                life=2.0,
                distance=100,
                end_size=60):
        '''
        Instantiate a new point burst and add it to the point burst list.
        '''
        new_pb = PointBurst(points, font, start_size, x_loc, y_loc, color, life, distance, end_size, self.pb_batch)
        self.pb_list.append(new_pb)


    def update_pbs(self, dt):
        '''
        Loop through all point bursts and call each one's update method.
        Build a list of dead ones for removal.
        '''
        self.dead_pbs = []
        for pb in self.pb_list:
            if not pb.dead:
                pb.update(dt)
            else:
                self.dead_pbs.append(pb)
        self.remove_dead_pbs()


    def remove_dead_pbs(self):
        '''
        Remove all the 'dead' point bursts. (ones that have faded out)
        Also, set their batch to none so that they will no longer be drawn.
        '''
        for pb in self.dead_pbs:
            pb.batch = None
            self.pb_list.remove(pb)



if __name__ == "__main__":

    window = pyglet.window.Window(1000, 700, caption="Points!")
    fps_display = pyglet.window.FPSDisplay(window)


    @window.event
    def on_mouse_press(x, y, button, modifiers):
        '''
        This function draws a somewhat randomized point burst wherever the mouse is clicked.
        '''
        pb_group.add_pb(points=randint(5, 10) * 10,
                        font='Arial',
                        start_size=15,
                        end_size=30,
                        x_loc=x,
                        y_loc=y,
                        color=get_random_color(),
                        life=1.0,
                        distance=50
                        )


    @window.event
    def on_draw():
        '''
        Clears the window, draw the point bursts and the fps display
        '''
        window.clear()
        pb_group.pb_batch.draw()
        fps_display.draw()


    def get_random_color():
        '''
        Utility function for getting a random color.
        '''
        return (randint(0, 255), randint(0, 255), randint(0, 255), 255)


    '''
    Create a point burst group, set the frames to update, and run the program.
    '''
    pb_group = PointBurstGroup()
    pyglet.clock.schedule_interval(pb_group.update_pbs, 1/120)
    pyglet.app.run()
