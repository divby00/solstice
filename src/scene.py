class Scene(object):

    def __init__(self, resourcemanager, scene_speed=40):
        self.font = resourcemanager.get('font')
        self.scene_speed = scene_speed
        self.running = False

    def render(self, scr):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')
