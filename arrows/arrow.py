import pyglet
from math import atan2, degrees


class Arrow(pyglet.sprite.Sprite):
    """
    Arrows are sprites that change their rotation to point at an x,y location
    on screen. They might be used to follow a mouse's motion around the screen.
    """
    def __init__(self, image, loc_x, loc_y, color, scale, batch):
        super(Arrow, self).__init__(img=image, x=loc_x, y=loc_y, batch=batch)
        self.color = color
        self.scale = scale

    def update_rotation(self, x, y):
        """
        Perform a little trigonometry to find the angle between the arrow's
        own location and the point it is meant to be pointing at.
        """
        adjacent = x - self.x
        opposite = (y - self.y) * -1
        angle = degrees(atan2(opposite, adjacent))
        self.rotation = angle


class ResourceImporter():
    """
    ResourceImporter is meant to simplify the importation of resources, such as
    sprite graphics.
    """
    def __init__(self, resource_path: str) -> 'ResourceImporter':
        pyglet.resource.path = [resource_path]
        pyglet.resource.reindex()

    def import_image(self, file_name: str) -> 'Image object':
        """Return a reference to a graphics file."""
        return pyglet.resource.image(file_name)

    def anchor_center(self, img: 'Image object') -> 'Image object':
        """Sets the image's center of rotation to the geometric center of the
        image itself."""
        img.anchor_x = img.width / 2
        img.anchor_y = img.height / 2
        return img


if __name__ == "__main__":
    window = pyglet.window.Window(500, 500)
    #window = pyglet.window.Window(fullscreen=True)
    main_batch = pyglet.graphics.Batch()
    fps_display = pyglet.window.FPSDisplay(window)


    @window.event
    def on_draw():
        window.clear()
        main_batch.draw()
        fps_display.draw()


    @window.event
    def on_mouse_motion(x, y, button, modifiers):
        """
        Send the current mouse x and y coords to each arrow to update itself.
        """
        for arrow in arrow_list:
            arrow.update_rotation(x, y)


    def update(dt):
        pass

    # Use a ResourceImporter instance to import the arrow image.
    res_imp = ResourceImporter('./img')
    arrow_img = res_imp.anchor_center(res_imp.import_image('arrow.gif'))
    # create and arrow list that we can loop through to update them.
    arrow_list = []
    arrow_list.append(Arrow(arrow_img, window.width/2, window.height/2, (0, 0, 153), 8.0, main_batch))
    for i in range(0, window.width+1, 30):
        for j in range(0, window.height+1, 30):
            arrow_list.append(Arrow(arrow_img, i, j, (255, 153, 0), 0.5, main_batch))


    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()
