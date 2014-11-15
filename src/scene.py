import pygame


class Scene(object):

    def __init__(self, context, scene_speed=40):
        self.scene_speed = scene_speed
        self.running = False
        self.cfg = context.cfg
        self.control = context.control
        self.font = context.resourcemanager.get('font')
        self.font_selected = context.resourcemanager.get('font_selected')
        self.blip = context.resourcemanager.get('blip')
        self.accept = context.resourcemanager.get('accept')
        self.cancel = context.resourcemanager.get('cancel')
        self.panel_imgs = []
        panel = ['panel0', 'panel1', 'panel2',
                 'panel3', 'panel4', 'panel5',
                 'panel6', 'panel7', 'panel8',
                 'cursor', 'font_dither']

        for p in xrange(0, len(panel)):
            self.panel_imgs.insert(p, context.resourcemanager.get(panel[p]))

        self.menu_context = (self.panel_imgs,
                             (self.font, self.font_selected),
                             (self.blip, self.accept, self.cancel),
                             self.control)

    def render(self, scr):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')
