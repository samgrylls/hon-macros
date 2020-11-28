from PyQt5.QtCore import QRunnable, pyqtSlot
import time
import window_functions as wf
from PIL import Image
import BoundingBox as bb


class CreepStack(QRunnable):
    """
    Base class for stacking creeps
    """

    def __init__(self, hon_window, creep_camps):
        """
        :param hon_window: current HonWindow object
        :param creep_camps: list of CreepCamp objects
        """
        super().__init__()
        self.hon_window = hon_window
        self.creep_camps = creep_camps
        self.creep_timer_image = Image.open('img/creep_pull_time.png')
        self.creep_healthbar_image = Image.open('img/creep_healthbar.png')

    @pyqtSlot()
    def run(self):
        self.move_to_camp(self.creep_camp)
        self.wait_for_stack()
        self.stack_camp()
        self.run_away()

    def move_to_camp(self, creep_camp):
        self.hon_window.right_click(creep_camp.location)
        while True:
            time.sleep(0.1)
            if self.check_arrival(creep_camp):
                print('arrived')
                break
        return None

    def wait_for_stack(self):
        while True:
            time.sleep(0.2)
            if wf.find_img_in_window(self.hon_window.screenshot(self.hon_window.clock), self.creep_timer_image).x > 0:
                print('time to stack')
                break
        return None

    def stack_camp(self):
        # need some better logic here to know exactly where to click the creep
        coords = self.find_creep()
        if coords.x > 0:
            self.hon_window.right_click(coords)
        time.sleep(0.5)

    def run_away(self):
        self.hon_window.right_click(self.creep_camp.run_away_coords)

    def check_arrival(self, creep_camp):
        hero_coords = self.hon_window.locate_hero()
        # print(hero_coords.as_dict())
        # print(self.creep_camp.location.x, self.creep_camp.location.y)
        return ((hero_coords.x < creep_camp.location.x)
                & (hero_coords.x + hero_coords.width > creep_camp.location.x)
                & (hero_coords.y < creep_camp.location.y)
                & (hero_coords.y + hero_coords.height > creep_camp.location.y))

    def find_creep(self, quadrant='bottom_left'):
        quadrant = self.hon_window.bounding_box.quadrant(quadrant)
        print(quadrant.as_dict())
        creep_location = wf.find_img_in_window(
            self.hon_window.quadrant_screenshot(quadrant),
            self.creep_healthbar_image
        )
        print(creep_location.as_dict())
        return bb.Point(creep_location.x + quadrant.x - self.hon_window.bounding_box.x,
                        creep_location.y + quadrant.y - self.hon_window.bounding_box.y)


class DoubleCreepStack(CreepStack):

    @pyqtSlot()
    def run(self):
        for creep in self.creep_camps:
            self.move_to_camp(creep[0])
            self.wait_for_stack()
            self.stack_camp()
        self.run_away()
