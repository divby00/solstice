import resmngr


class Scene(object):

    def __init__(self, rmngr, scene_speed=40):
        self.font = rmngr.get('font')
        self.scene_speed = scene_speed
        self.running = False

    def render(self, virt):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')
