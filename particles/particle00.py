import pyglet
import math
import random


class Particle(pyglet.sprite.Sprite):
    """
    Particle is a (probably small) sprite that keeps track of itself and
    marks itself for removal at the proper time. It is meant to be created by
    a ParticleEmitter, which has the code for determining the particle's
    characteristics.
    """
    def __init__(self,
                 image,
                 loc_x,
                 loc_y,
                 my_batch,
                 color=(255, 255, 255),
                 opacity=255,
                 rotation=0,
                 scale=1.0,
                 speed=50,
                 direction=0,
                 life=1.0,
                ):
        super(Particle, self).__init__(img=image, x=loc_x, y=loc_y, batch=my_batch)
        self.color = color
        self.opacity = opacity
        self.rotation = rotation
        self.scale = scale
        self.speed = speed
        self.direction = direction
        self.dx, self.dy = self.get_dx_dy(self.speed, self.direction)
        self.life = life
        self.age = 0.0

        self.dead = False

    def get_dx_dy(self, speed, direction):
        """
        Find the change per second in x and y coords,
        based on speed and direction.
        """
        rads = math.radians(direction)
        dx = math.cos(rads) * speed
        dy = math.sin(rads) * speed
        return (dx, dy)


    def update_loc(self, dt):
        """
        Perform the changes in x and y coords.
        """
        self.x = self.x + (self.dx * dt)
        self.y = self.y + (self.dy * dt)


    def update(self, dt):
        """
        Calls other update methods, and calculates particle's age,
        which determines wether it is time to declare itself 'dead' yet.
        When a particle is 'dead', the Emmiter removes it from its list of
        active particles, and the particle removes itself from it's graphics
        batch, which means Python's garbage collection releases it from
        memory.
        """
        self.update_loc(dt)
        self.age += dt
        if self.age > self.life:
            self.dead = True
            self.batch = None
            del self


class ParticleEmitter():
    """
    ParticleEmitters create Particles. They have x and y coords, which tell the
    particles where they start from, and a dictionary of values that describe
    the characteristics of the Emitter's particles. Some of these can be
    ranges of values, so the particles have variation. Emitters keep a list of
    active particles, and remove 'dead' ones from the list.
    """
    def __init__(self,
                 x: int,
                 y: int,
                 particle_chars: dict):
        self.x = x
        self.y = y
        self.image = particle_chars["img"]
        self.color = particle_chars["color"]
        self.opacity_min, self.opacity_max = particle_chars["opacity"]
        self.rotation_min, self.rotation_max = particle_chars["rotation"]
        self.scale_min, self.scale_max = particle_chars["scale"]
        self.speed_min, self.speed_max = particle_chars["speed"]
        self.direction_min, self.direction_max = particle_chars["direction"]
        self.life_min, self.life_max = particle_chars["life"]
        self.batch = particle_chars["batch"]
        self.particle_list = []


    def add_particle(self, dt):
        """
        Instantiates a new particle and adds it to the Emitter's particle list.
        """
        new_particle = Particle(image=self.image,
                                loc_x=self.x,
                                loc_y=self.y,
                                my_batch=self.batch,
                                color=self.color,
                                opacity=random.randint(self.opacity_min, self.opacity_max),
                                rotation=random.randint(self.rotation_min, self.rotation_max),
                                scale=(random.randint(self.scale_min * 100, self.scale_max * 100))/100.0,
                                speed=random.randint(self.speed_min, self.speed_max),
                                direction=random.randint(self.direction_min, self.direction_max),
                                life=(random.randint(self.life_min * 100, self.life_max * 100))/100.0,
                                )
        self.particle_list.append(new_particle)


    def update(self, dt):
        """
        Loops throug the Emitter's particle list, updating 'non-dead' particles,
        and removing 'dead' particles.
        """
        for particle in self.particle_list:
            particle.update(dt)
            if particle.dead:
                self.particle_list.remove(particle)


if __name__ == "__main__":
    window = pyglet.window.Window()
    fps_display = pyglet.window.FPSDisplay(window)

    # import some graphics to use for particles.
    pyglet.resource.path = ['./img']
    pyglet.resource.reindex()

    particle_image = pyglet.resource.image('particle.gif')
    particle_image.anchor_x = particle_image.width / 2
    particle_image.anchor_y = particle_image.height / 2

    particle_image2 = pyglet.resource.image('particle2.gif')
    particle_image2.anchor_x = particle_image2.width / 2
    particle_image2.anchor_y = particle_image2.height / 2

    particle_image3 = pyglet.resource.image('particle5.png')
    particle_image3.anchor_x = particle_image2.width / 2
    particle_image3.anchor_y = particle_image2.height / 2


    def get_random_color():
        """
        Utility function for selecting random colors in the RGB color model.
        """
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # create a graphics batch for pyglet to use in drawing the particles.
    my_batch = pyglet.graphics.Batch()

    """
    Make a pair of dicts describing two very different types of Particles,
    and instantiate a pair of ParticleEmitters to emit them
    """
    particle_dict = {   "img": particle_image3,
                        "color": (102, 102, 102),#get_random_color(),
                        "opacity": (51, 153),
                        "rotation": (0, 0),
                        "scale": (0.5, 1.5),
                        "speed": (50, 100),
                        "direction": (80, 140),
                        "life": (20.0, 20.0),
                        "batch": my_batch
    }
    part_emit = ParticleEmitter(window.width/2, window.height/6, particle_dict)

    particle_dict2 = {  "img": particle_image2,
                        "color": (255, 255, 255),
                        "opacity": (255, 255),
                        "rotation": (0, 0),
                        "scale": (1.0, 1.0),
                        "speed": (300, 300),
                        "direction": (0, 0),
                        "life": (4.0, 4.0),
                        "batch": my_batch
    }
    part_emit2 = ParticleEmitter(window.width/6, window.height/2, particle_dict2)

    @window.event
    def on_draw():
        window.clear()
        my_batch.draw()
        fps_display.draw()


    def update(dt):
        part_emit.update(dt)
        part_emit2.update(dt)

    pyglet.clock.schedule_interval(part_emit.add_particle, 1/60)
    pyglet.clock.schedule_interval(part_emit2.add_particle, 1/6)
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()
