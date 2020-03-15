class BoundingBox:
    def __init__(self, coords, mode='corners'):
        if mode == 'corners':
            self.x = coords[0]
            self.y = coords[1]
            self.width = coords[2] - coords[0]
            self.height = coords[3] - coords[1]
        elif mode == 'relative':
            self.x = coords[0]
            self.y = coords[1]
            self.width = coords[2]
            self.height = coords[3]

    def as_dict(self):
        bb_dict_keys = ['left', 'top', 'width', 'height']
        return dict(zip(bb_dict_keys, [self.x, self.y, self.width, self.height]))

    def quadrant(self, quadrant):
        if quadrant == 'top_left':
            return BoundingBox([self.x, self.y, self.width//2, self.height//2], mode='relative')
        elif quadrant == 'top_right':
            return BoundingBox([self.x + self.width//2, self.y, self.width//2, self.height//2], mode='relative')
        elif quadrant == 'bottom_left':
            return BoundingBox([self.x, self.y + self.height//2, self.width//2, self.height//2], mode='relative')
        elif quadrant == 'bottom_right':
            return BoundingBox([self.x + self.width//2, self.y + self.height//2, self.width//2, self.height//2],
                               mode='relative')
        else:
            raise ValueError('Invalid quadrant specified')


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class CreepCamp:
    def __init__(self, location, run_away_coords):
        self.location = location
        self.run_away_coords = run_away_coords