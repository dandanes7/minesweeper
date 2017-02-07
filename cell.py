class Cell():
    def __init__(self):
        self.touched = False
        self.has_mine = False
        self.marked = False
        self.value = 0

    def _place_mine(self):
        self.has_mine = True

    def touch(self):
        if not self.marked:
            self.touched = True
            return self.has_mine

    def mark_as_safe(self):
        if not self.touched:
            self.marked = True

    def unmark(self):
        if self.marked:
            self.marked = False
