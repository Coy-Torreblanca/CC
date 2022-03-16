#!/usr/bin/env python3

from cc import turtle, import_file, gps

# globals
refuel = import_file("/lib/fuel.py").refuel
direction_map, refuel_cost = import_file("data/nav.py").get_data()


class nav:
    direction = "north"
    direction_test_pass = False

    def __init__(self):
        self.direction_test_pass = self.direction_test()

    def direction_test():
        # west is negative x
        # north is negative z
        # xyz
        position = gps.locate()

        if position[0]:

            if self.forward():
                position2 = gps.locate()
                if position2[0] - position[0] < 0:
                    self.direction = "west"
                    return True
                elif position2[0] - position[0] > 0:
                    self.direction = "east"
                    return True
                elif position2[2] - position[2] > 0:
                    self.direction = "south"
                    return True
                elif position2[2] - position[2] < 0:
                    self.direction = "north"
                    return True
            return False

    def call_move(self, move):

        try:
            move()

        except BaseException as error:
            if error == "Out of fuel":
                refuel.refuel()

            try:
                if not move():
                    return False
            except:
                return False

        return True

    def up(self):
        return self.call_move(turtle.up)

    def down(self):
        return self.call_move(turtle.down)

    def forward(self):
        return self.call_move(turtle.forward)

    def back(self):
        return self.call_move(turtle.back)

    def turn_left(self):
        self.direction = direction_map[self.direction]["left"]
        return turtle.turnLeft()

    def turn_right(self):
        self.direction = direction_map[self.direction]["right"]
        return turtle.turnRight()

    def turn_to(self, to_direction):
        while self.direction != to_direction:
            self.turn_right()
        return True

    def locate(self):
        return gps.locate()
