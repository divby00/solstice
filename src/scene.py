class Scene(object):

    def __init__(self, context, scene_speed=40):
        self.cfg = context.cfg
        self.font = context.resourcemanager.get('font')
        self.font_selected = context.resourcemanager.get('font_selected')
        self.scene_speed = scene_speed
        self.running = False
        self.panel_imgs = []
        panel = ['panel0', 'panel1', 'panel2',
                 'panel3', 'panel4', 'panel5',
                 'panel6', 'panel7', 'panel8',
                 'cursor']

        for p in xrange(0, len(panel)):
            self.panel_imgs.insert(p, context.resourcemanager.get(panel[p]))

    def render(self, scr):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')
