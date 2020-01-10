class FakeRoom(object):
    def __init__(self, id, title, description, x, y, n_to = None, e_to = None, s_to = None, w_to = None):
        self.id = id
        self.title = title
        self.description = description
        self.x = x
        self.y = y
        self.n_to = n_to
        self.e_to = e_to
        self.s_to = s_to
        self.w_to = w_to