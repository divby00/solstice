class Container(object):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.secured = False


class ContainerBuilder(object):

    @staticmethod
    def build(container_info):
        info = container_info.split(' ')
        return Container(int(info[0]), int(info[1]), int(info[2]), int(info[3]))