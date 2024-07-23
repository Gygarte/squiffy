class DefaultBorderStyle:
    @property
    def top_horizontal(self):
        return "─"

    @property
    def bottom_horizontal(self):
        return "─"

    @property
    def left_vertical(self):
        return "│"

    @property
    def right_vertical(self):
        return "│"

    @property
    def top_left_corner(self):
        return "┌"

    @property
    def top_right_corner(self):
        return "┐"

    @property
    def bottom_left_corner(self):
        return "└"

    @property
    def bottom_right_corner(self):
        return "┘"

    @property
    def horizontal(self):
        return "─"

    @property
    def vertical(self):
        return "│"

    @property
    def intersection(self):
        return "┼"

    @property
    def right_intersection(self):
        return "├"

    @property
    def left_intersection(self):
        return "┤"
